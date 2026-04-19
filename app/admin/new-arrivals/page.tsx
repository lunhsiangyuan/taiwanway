'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import type { Product } from '@/types/product';

const ADMIN_PW_KEY = 'tw-admin-pw';

function getPassword(): string {
  if (typeof window === 'undefined') return '';
  return sessionStorage.getItem(ADMIN_PW_KEY) || '';
}

function adminHeaders(): Record<string, string> {
  return { 'x-admin-password': getPassword(), 'Content-Type': 'application/json' };
}

function LoginForm({ onLogin }: { onLogin: () => void }) {
  const [pw, setPw] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    const res = await fetch('/api/auth/verify', {
      method: 'POST',
      headers: { 'x-admin-password': pw },
    });
    if (res.ok) {
      sessionStorage.setItem(ADMIN_PW_KEY, pw);
      onLogin();
    } else {
      setError('密碼錯誤');
      sessionStorage.removeItem(ADMIN_PW_KEY);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h1 className="text-xl font-bold mb-4">New Arrival 管理</h1>
        <input
          type="password"
          placeholder="密碼"
          value={pw}
          onChange={(e) => setPw(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
          className="w-full border rounded px-3 py-2 mb-3"
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button
          onClick={handleLogin}
          className="w-full bg-amber-800 text-white py-2 rounded hover:bg-amber-900"
        >
          登入
        </button>
      </div>
    </div>
  );
}

export default function NewArrivalsAdmin() {
  const [authed, setAuthed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState<Product[]>([]);
  const [featuredUntil, setFeaturedUntil] = useState<string>('');
  const [savingIds, setSavingIds] = useState<Set<string>>(new Set());
  const [toast, setToast] = useState<string>('');

  // 檢查 session 是否已登入
  useEffect(() => {
    if (!getPassword()) {
      setLoading(false);
      return;
    }
    fetch('/api/auth/verify', {
      method: 'POST',
      headers: { 'x-admin-password': getPassword() },
    })
      .then((r) => {
        if (r.ok) {
          setAuthed(true);
        } else {
          sessionStorage.removeItem(ADMIN_PW_KEY);
        }
      })
      .finally(() => setLoading(false));
  }, []);

  // 載入商品
  useEffect(() => {
    if (!authed) return;
    fetch('/api/products', { headers: adminHeaders() })
      .then((r) => r.json())
      .then((data: Product[]) => {
        if (Array.isArray(data)) {
          setProducts(data);
          // 預設 featuredUntil 為本月月底
          const today = new Date();
          const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
          setFeaturedUntil(endOfMonth.toISOString().slice(0, 10));
        }
      });
  }, [authed]);

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(''), 2000);
  };

  const toggleNewArrival = async (p: Product) => {
    const newValue = !p.is_new_arrival;
    setSavingIds((s) => new Set(s).add(p.id));

    const payload: Record<string, unknown> = {
      id: p.id,
      is_new_arrival: newValue,
    };
    // 勾選時一併寫入截止日期；取消勾選時清空
    if (newValue && featuredUntil) {
      payload.featured_until = featuredUntil;
    } else if (!newValue) {
      payload.featured_until = null;
    }

    const res = await fetch('/api/products', {
      method: 'PATCH',
      headers: adminHeaders(),
      body: JSON.stringify(payload),
    });

    setSavingIds((s) => {
      const next = new Set(s);
      next.delete(p.id);
      return next;
    });

    if (res.ok) {
      const updated = await res.json();
      setProducts((prev) => prev.map((x) => (x.id === p.id ? updated : x)));
      showToast(newValue ? '已加入本月新品' : '已從新品區移除');
    } else {
      showToast('儲存失敗');
    }
  };

  // 批次更新所有已勾選的 featured_until
  const applyFeaturedUntilToAll = async () => {
    if (!featuredUntil) return;
    const toUpdate = products.filter((p) => p.is_new_arrival);
    if (toUpdate.length === 0) {
      showToast('目前沒有新品，請先勾選');
      return;
    }
    for (const p of toUpdate) {
      await fetch('/api/products', {
        method: 'PATCH',
        headers: adminHeaders(),
        body: JSON.stringify({ id: p.id, featured_until: featuredUntil }),
      });
    }
    // 重新載入
    const r = await fetch('/api/products', { headers: adminHeaders() });
    const data = await r.json();
    setProducts(data);
    showToast(`已更新 ${toUpdate.length} 個新品的截止日期`);
  };

  if (loading) return <div className="p-8 text-center text-gray-400">載入中...</div>;
  if (!authed) return <LoginForm onLogin={() => setAuthed(true)} />;

  const newArrivalCount = products.filter((p) => p.is_new_arrival).length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-4">
          <h1 className="text-lg font-bold text-amber-900 flex-1">🆕 New Arrival 管理</h1>
          <Link href="/admin/products" className="text-sm text-amber-700 hover:underline">
            ← 回產品管理
          </Link>
          <button
            onClick={() => {
              sessionStorage.removeItem(ADMIN_PW_KEY);
              setAuthed(false);
            }}
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            登出
          </button>
        </div>
      </div>

      {/* Control bar */}
      <div className="bg-amber-50 border-b border-amber-200">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <div className="flex flex-wrap items-center gap-3 text-sm">
            <div className="font-semibold text-amber-900">
              目前新品：<span className="text-lg">{newArrivalCount}</span> 項
            </div>
            <span className="text-amber-600">|</span>
            <label className="flex items-center gap-2">
              <span className="text-amber-800">本月截止日：</span>
              <input
                type="date"
                value={featuredUntil}
                onChange={(e) => setFeaturedUntil(e.target.value)}
                className="border border-amber-300 rounded px-2 py-1 bg-white"
              />
            </label>
            <button
              onClick={applyFeaturedUntilToAll}
              className="bg-amber-700 text-white px-3 py-1.5 rounded hover:bg-amber-800 text-xs"
            >
              套用到所有已勾選的新品
            </button>
          </div>
          <p className="text-xs text-amber-700 mt-2">
            💡 勾選下方商品會立刻上架到首頁 <strong>New Arrival 本月新品</strong> 區塊。超過截止日期會自動下架。
          </p>
        </div>
      </div>

      {/* Product grid */}
      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {products.map((p) => {
            const isSaving = savingIds.has(p.id);
            const isNew = !!p.is_new_arrival;
            return (
              <button
                key={p.id}
                onClick={() => toggleNewArrival(p)}
                disabled={isSaving}
                className={`relative text-left bg-white rounded-xl overflow-hidden shadow-sm transition-all ${
                  isNew
                    ? 'ring-2 ring-amber-500 shadow-md'
                    : 'ring-1 ring-gray-200 hover:ring-amber-300'
                } ${isSaving ? 'opacity-50' : ''}`}
              >
                {/* NEW badge */}
                {isNew && (
                  <div className="absolute top-2 right-2 z-10 bg-amber-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow">
                    NEW
                  </div>
                )}
                <div className="relative aspect-square bg-gray-50">
                  <Image
                    src={p.image_url}
                    alt={p.name_zh}
                    fill
                    className="object-contain p-2"
                    sizes="(max-width: 640px) 50vw, 25vw"
                    loading="lazy"
                  />
                </div>
                <div className="p-3">
                  {p.brand && (
                    <p className="text-[10px] text-amber-600 uppercase tracking-wider truncate">
                      {p.brand}
                    </p>
                  )}
                  <h3 className="font-semibold text-sm text-amber-950 leading-tight line-clamp-2 mt-0.5">
                    {p.name_zh}
                  </h3>
                  {p.price != null && (
                    <p className="font-bold text-amber-800 text-sm mt-1">
                      ${Number(p.price).toFixed(2)}
                    </p>
                  )}
                  <div
                    className={`mt-2 text-xs font-medium ${
                      isNew ? 'text-amber-700' : 'text-gray-400'
                    }`}
                  >
                    {isNew ? '✓ 本月新品' : '點一下加入新品'}
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {products.length === 0 && (
          <p className="text-center text-gray-400 py-12">沒有商品資料</p>
        )}
      </div>

      {/* Toast */}
      {toast && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 bg-amber-900 text-white px-4 py-2 rounded-full shadow-lg text-sm">
          {toast}
        </div>
      )}
    </div>
  );
}
