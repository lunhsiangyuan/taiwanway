'use client';

import { useEffect, useState, useRef } from 'react';
import Image from 'next/image';
import type { Product } from '@/types/product';

const ADMIN_PW_KEY = 'tw-admin-pw';



function getPassword(): string {
  if (typeof window === 'undefined') return '';
  return sessionStorage.getItem(ADMIN_PW_KEY) || '';
}

function adminHeaders(): Record<string, string> {
  return { 'x-admin-password': getPassword(), 'Content-Type': 'application/json' };
}

// ---- Login ----
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
        <h1 className="text-xl font-bold mb-4">產品管理後台</h1>
        <input
          type="password"
          placeholder="密碼"
          value={pw}
          onChange={(e) => setPw(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
          className="w-full border rounded px-3 py-2 mb-3"
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button onClick={handleLogin} className="w-full bg-amber-800 text-white py-2 rounded hover:bg-amber-900">
          登入
        </button>
      </div>
    </div>
  );
}

// ---- Product Form ----
function ProductForm({
  initial,
  onSave,
  onCancel,
}: {
  initial?: Partial<Product>;
  onSave: (data: Record<string, unknown>) => Promise<void>;
  onCancel: () => void;
}) {
  const [form, setForm] = useState({
    slug: initial?.slug || '',
    brand: initial?.brand || '',
    price: initial?.price?.toString() || '',
    origin: initial?.origin || '',
    name_zh: initial?.name_zh || '',
    name_en: initial?.name_en || '',
    name_es: initial?.name_es || '',
    description_zh: initial?.description_zh || '',
    description_en: initial?.description_en || '',
    description_es: initial?.description_es || '',
    how_to_use_zh: initial?.how_to_use_zh || '',
    how_to_use_en: initial?.how_to_use_en || '',
    how_to_use_es: initial?.how_to_use_es || '',
    image_url: initial?.image_url || '',
  });
  const [uploading, setUploading] = useState(false);
  
  const [saving, setSaving] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const set = (key: string, val: string) => setForm((f) => ({ ...f, [key]: val }));

  const handleUpload = async (file: File) => {
    setUploading(true);
    const fd = new FormData();
    fd.append('file', file);
    const res = await fetch('/api/products/upload', {
      method: 'POST',
      headers: { 'x-admin-password': getPassword() },
      body: fd,
    });
    const data = await res.json();
    if (data.url) set('image_url', data.url);
    setUploading(false);
  };


  const handleSave = async () => {
    if (!form.slug || !form.name_zh || !form.name_en || !form.name_es || !form.image_url) {
      return alert('缺少必填欄位（slug, 三語名稱, 圖片）');
    }
    setSaving(true);
    await onSave({
      ...form,
      price: form.price ? parseFloat(form.price) : null,
      ...(initial?.id ? { id: initial.id } : {}),
    });
    setSaving(false);
  };

  return (
    <div className="space-y-4">
      {/* Image upload */}
      <div>
        <label className="block text-sm font-medium mb-1">產品照片</label>
        <div className="flex items-center gap-4">
          {form.image_url && (
            <div className="relative w-24 h-24 rounded border overflow-hidden">
              <Image src={form.image_url} alt="product" fill className="object-cover" sizes="96px" />
            </div>
          )}
          <div>
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files?.[0] && handleUpload(e.target.files[0])} />
            <button onClick={() => fileRef.current?.click()} disabled={uploading} className="bg-gray-200 px-3 py-1 rounded text-sm hover:bg-gray-300">
              {uploading ? '上傳中...' : '選擇照片'}
            </button>
          </div>
        </div>
      </div>


      {/* Basic info */}
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="block text-sm font-medium mb-1">Slug (URL)</label>
          <input value={form.slug} onChange={(e) => set('slug', e.target.value)} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">品牌</label>
          <input value={form.brand} onChange={(e) => set('brand', e.target.value)} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">價格 ($)</label>
          <input type="number" step="0.01" value={form.price} onChange={(e) => set('price', e.target.value)} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">產地</label>
          <input value={form.origin} onChange={(e) => set('origin', e.target.value)} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
      </div>

      {/* Names */}
      <div className="grid grid-cols-3 gap-3">
        {(['zh', 'en', 'es'] as const).map((lang) => (
          <div key={lang}>
            <label className="block text-sm font-medium mb-1">名稱 ({lang.toUpperCase()})</label>
            <input value={form[`name_${lang}`]} onChange={(e) => set(`name_${lang}`, e.target.value)} className="w-full border rounded px-2 py-1 text-sm" />
          </div>
        ))}
      </div>

      {/* Descriptions */}
      {(['zh', 'en', 'es'] as const).map((lang) => (
        <div key={lang}>
          <label className="block text-sm font-medium mb-1">介紹 ({lang.toUpperCase()})</label>
          <textarea value={form[`description_${lang}`]} onChange={(e) => set(`description_${lang}`, e.target.value)} rows={3} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
      ))}

      {/* How to use */}
      {(['zh', 'en', 'es'] as const).map((lang) => (
        <div key={lang}>
          <label className="block text-sm font-medium mb-1">食用方式 ({lang.toUpperCase()})</label>
          <textarea value={form[`how_to_use_${lang}`]} onChange={(e) => set(`how_to_use_${lang}`, e.target.value)} rows={2} className="w-full border rounded px-2 py-1 text-sm" />
        </div>
      ))}

      {/* Actions */}
      <div className="flex gap-3 pt-2">
        <button onClick={handleSave} disabled={saving} className="bg-amber-800 text-white px-6 py-2 rounded hover:bg-amber-900 disabled:opacity-50">
          {saving ? '儲存中...' : initial?.id ? '更新' : '新增產品'}
        </button>
        <button onClick={onCancel} className="bg-gray-200 px-4 py-2 rounded hover:bg-gray-300">
          取消
        </button>
      </div>
    </div>
  );
}

// ---- QR Print View ----
function QRPrintView({ products, onClose }: { products: Product[]; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-white z-50 overflow-auto print:static">
      <div className="no-print p-4 flex gap-3 border-b">
        <button onClick={() => window.print()} className="bg-amber-800 text-white px-4 py-2 rounded">
          🖨️ 列印
        </button>
        <button onClick={onClose} className="bg-gray-200 px-4 py-2 rounded">
          關閉
        </button>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 p-4 print:grid-cols-3 print:gap-2 print:p-2">
        {products.map((p) => (
          <div key={p.id} className="border rounded-lg p-4 flex flex-col items-center text-center print:border-gray-300 print:p-3 break-inside-avoid">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={`/api/products/qr?slug=${p.slug}`} alt={`QR ${p.slug}`} className="w-32 h-32 print:w-28 print:h-28" />
            <p className="mt-2 font-bold text-sm">{p.name_zh}</p>
            <p className="text-xs text-gray-600">{p.name_en}</p>
            {p.price && <p className="text-sm font-bold mt-1">${Number(p.price).toFixed(2)}</p>}
            <p className="text-[10px] text-gray-400 mt-1">Scan to learn more · 掃碼了解更多</p>
          </div>
        ))}
      </div>
      <style>{`
        @media print {
          .no-print { display: none !important; }
          body { padding: 0; margin: 0; }
        }
      `}</style>
    </div>
  );
}

// ---- Main Page ----
export default function AdminProductsPage() {
  const [authed, setAuthed] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'list' | 'add' | 'edit'>('list');
  const [editProduct, setEditProduct] = useState<Product | null>(null);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [showPrint, setShowPrint] = useState(false);

  useEffect(() => {
    if (getPassword()) {
      fetch('/api/products', { headers: { 'x-admin-password': getPassword() } })
        .then((r) => {
          if (r.ok) { setAuthed(true); return r.json(); }
          throw new Error();
        })
        .then((data) => setProducts(data || []))
        .catch(() => sessionStorage.removeItem(ADMIN_PW_KEY))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const loadProducts = async () => {
    const res = await fetch('/api/products', { headers: { 'x-admin-password': getPassword() } });
    const data = await res.json();
    setProducts(data || []);
  };

  const handleCreate = async (data: Record<string, unknown>) => {
    const res = await fetch('/api/products', { method: 'POST', headers: adminHeaders(), body: JSON.stringify(data) });
    if (res.ok) { await loadProducts(); setView('list'); }
    else { const e = await res.json(); alert(e.error || 'Failed'); }
  };

  const handleUpdate = async (data: Record<string, unknown>) => {
    const res = await fetch('/api/products', { method: 'PATCH', headers: adminHeaders(), body: JSON.stringify(data) });
    if (res.ok) { await loadProducts(); setView('list'); setEditProduct(null); }
    else { const e = await res.json(); alert(e.error || 'Failed'); }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('確定停用這個產品？')) return;
    await fetch('/api/products', { method: 'DELETE', headers: adminHeaders(), body: JSON.stringify({ id }) });
    await loadProducts();
  };

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      return next;
    });
  };

  const selectAll = () => {
    if (selectedIds.size === products.length) setSelectedIds(new Set());
    else setSelectedIds(new Set(products.map((p) => p.id)));
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  if (!authed) return <LoginForm onLogin={() => { setAuthed(true); loadProducts(); }} />;

  if (showPrint) {
    const printProducts = selectedIds.size > 0 ? products.filter((p) => selectedIds.has(p.id)) : products.filter((p) => p.is_active);
    return <QRPrintView products={printProducts} onClose={() => setShowPrint(false)} />;
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">產品管理</h1>
        <div className="flex gap-2">
          {view === 'list' && (
            <>
              <button onClick={() => setView('add')} className="bg-amber-800 text-white px-4 py-2 rounded text-sm hover:bg-amber-900">
                + 新增產品
              </button>
              <button onClick={() => setShowPrint(true)} className="bg-gray-200 px-4 py-2 rounded text-sm hover:bg-gray-300">
                🖨️ 列印 QR Code {selectedIds.size > 0 ? `(${selectedIds.size})` : ''}
              </button>
            </>
          )}
        </div>
      </div>

      {view === 'add' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-bold mb-4">新增產品</h2>
          <ProductForm onSave={handleCreate} onCancel={() => setView('list')} />
        </div>
      )}

      {view === 'edit' && editProduct && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-bold mb-4">編輯：{editProduct.name_zh}</h2>
          <ProductForm initial={editProduct} onSave={handleUpdate} onCancel={() => { setView('list'); setEditProduct(null); }} />
        </div>
      )}

      {view === 'list' && (
        <div>
          <div className="mb-3 flex items-center gap-2">
            <input type="checkbox" checked={selectedIds.size === products.length && products.length > 0} onChange={selectAll} />
            <span className="text-sm text-gray-500">全選 ({products.length} 個產品)</span>
          </div>
          <div className="space-y-3">
            {products.map((p) => (
              <div key={p.id} className={`bg-white rounded-lg shadow p-4 flex gap-4 items-start ${!p.is_active ? 'opacity-50' : ''}`}>
                <input type="checkbox" checked={selectedIds.has(p.id)} onChange={() => toggleSelect(p.id)} className="mt-2" />
                <div className="relative w-16 h-16 rounded overflow-hidden shrink-0 bg-gray-100">
                  {p.image_url && <Image src={p.image_url} alt={p.name_en} fill className="object-cover" sizes="64px" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-bold">{p.name_zh}</p>
                      <p className="text-sm text-gray-600">{p.name_en}</p>
                      {p.brand && <p className="text-xs text-gray-400">{p.brand}</p>}
                    </div>
                    <div className="text-right shrink-0">
                      {p.price && <p className="font-bold text-amber-800">${Number(p.price).toFixed(2)}</p>}
                      {!p.is_active && <span className="text-xs text-red-500">已停用</span>}
                    </div>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">/{p.slug}</p>
                  <div className="flex gap-2 mt-2">
                    <button
                      onClick={() => { setEditProduct(p); setView('edit'); }}
                      className="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
                    >
                      ✏️ 編輯
                    </button>
                    <a
                      href={`/product/${p.slug}`}
                      target="_blank"
                      className="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
                    >
                      👁️ 預覽
                    </a>
                    <a
                      href={`/api/products/qr?slug=${p.slug}`}
                      target="_blank"
                      className="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
                    >
                      📱 QR Code
                    </a>
                    {p.is_active && (
                      <button
                        onClick={() => handleDelete(p.id)}
                        className="text-xs bg-red-50 text-red-600 px-2 py-1 rounded hover:bg-red-100"
                      >
                        🗑️ 停用
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {products.length === 0 && (
              <p className="text-center text-gray-400 py-8">還沒有產品，按上方「+ 新增產品」開始</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
