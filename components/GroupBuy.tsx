'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { useLanguage } from '@/lib/i18n/language-context';

// Types
interface GroupBuyItem {
  id: string;
  name: {
    zh: string;
    en: string;
    es: string;
  };
  description: {
    zh: string;
    en: string;
    es: string;
  };
  image: string;
  currentOrders: number;
  targetOrders: number;
  deadline: string;
  price: number;
  unit: string;
  formUrl?: string;
}

// Mock Data - Replace with API call later
const MOCK_GROUP_BUYS: GroupBuyItem[] = [
  {
    id: '1',
    name: {
      zh: '台灣鳳梨酥禮盒',
      en: 'Taiwan Pineapple Cake Gift Box',
      es: 'Caja de Regalo de Pastel de Piña de Taiwán',
    },
    description: {
      zh: '道地台灣鳳梨酥，酥脆外皮配上香甜鳳梨內餡，12入精美禮盒裝',
      en: 'Authentic Taiwan pineapple cakes with crispy crust and sweet filling, 12pcs gift box',
      es: 'Pasteles de piña auténticos de Taiwán, caja de regalo de 12 piezas',
    },
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg',
    currentOrders: 18,
    targetOrders: 30,
    deadline: '2026-02-14',
    price: 25,
    unit: 'box',
  },
  {
    id: '2',
    name: {
      zh: '手工水餃 (50入)',
      en: 'Handmade Dumplings (50pcs)',
      es: 'Dumplings Hechos a Mano (50 piezas)',
    },
    description: {
      zh: '新鮮手工包製，高麗菜豬肉餡，冷凍宅配到府',
      en: 'Fresh handmade dumplings with cabbage & pork filling, frozen delivery',
      es: 'Dumplings frescos hechos a mano, entrega congelada',
    },
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg',
    currentOrders: 25,
    targetOrders: 50,
    deadline: '2026-02-10',
    price: 35,
    unit: 'pack',
  },
];

// GroupBuyCard Component
function GroupBuyCard({ item, language }: { item: GroupBuyItem; language: string }) {
  const lang = language as keyof typeof item.name;
  const progress = Math.min((item.currentOrders / item.targetOrders) * 100, 100);
  const daysLeft = Math.max(0, Math.ceil((new Date(item.deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24)));

  const deadlineText = {
    zh: `剩餘 ${daysLeft} 天`,
    en: `${daysLeft} days left`,
    es: `${daysLeft} días restantes`,
  };

  const ordersText = {
    zh: `${item.currentOrders}/${item.targetOrders} 份已訂購`,
    en: `${item.currentOrders}/${item.targetOrders} ordered`,
    es: `${item.currentOrders}/${item.targetOrders} pedidos`,
  };

  const orderNowText = {
    zh: '立即訂購',
    en: 'Order Now',
    es: 'Pedir Ahora',
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-orange-100 hover:shadow-xl transition-shadow duration-300">
      {/* Image */}
      <div className="relative h-48 w-full">
        <Image
          src={item.image}
          alt={item.name[lang]}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, 50vw"
        />
        {/* Deadline Badge */}
        <div className="absolute top-3 right-3 bg-orange-500 text-white px-3 py-1 rounded-full text-sm font-medium">
          {deadlineText[lang]}
        </div>
      </div>

      {/* Content */}
      <div className="p-5">
        <h3 className="text-xl font-bold text-gray-800 mb-2">{item.name[lang]}</h3>
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">{item.description[lang]}</p>

        {/* Price */}
        <div className="flex items-baseline gap-1 mb-4">
          <span className="text-2xl font-bold text-orange-600">${item.price}</span>
          <span className="text-gray-500 text-sm">/ {item.unit}</span>
        </div>

        {/* Progress Bar */}
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>{ordersText[lang]}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-gradient-to-r from-orange-400 to-orange-600 h-2.5 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* CTA Button */}
        <a
          href={item.formUrl || '#'}
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full bg-orange-500 hover:bg-orange-600 text-white text-center py-3 rounded-xl font-medium transition-colors duration-200"
        >
          {orderNowText[lang]}
        </a>
      </div>
    </div>
  );
}

// Loading Skeleton
function GroupBuyCardSkeleton() {
  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-orange-100 animate-pulse">
      <div className="h-48 bg-gray-200" />
      <div className="p-5">
        <div className="h-6 bg-gray-200 rounded mb-2 w-3/4" />
        <div className="h-4 bg-gray-200 rounded mb-4 w-full" />
        <div className="h-8 bg-gray-200 rounded mb-4 w-1/3" />
        <div className="h-2.5 bg-gray-200 rounded-full mb-4" />
        <div className="h-12 bg-gray-200 rounded-xl" />
      </div>
    </div>
  );
}

// Main GroupBuy Component
export function GroupBuy() {
  const { language } = useLanguage();
  const [items, setItems] = useState<GroupBuyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const sectionTitle = {
    zh: '團購專區',
    en: 'Group Buy',
    es: 'Compra Grupal',
  };

  const sectionSubtitle = {
    zh: '限時優惠，揪團一起買更划算！',
    en: 'Limited time offers - better deals when you order together!',
    es: '¡Ofertas por tiempo limitado - mejores precios juntos!',
  };

  const emptyText = {
    zh: '目前沒有進行中的團購活動，敬請期待！',
    en: 'No active group buys at the moment. Stay tuned!',
    es: '¡No hay compras grupales activas. ¡Estén atentos!',
  };

  const errorText = {
    zh: '載入失敗，請稍後再試',
    en: 'Failed to load. Please try again later.',
    es: 'Error al cargar. Por favor, inténtelo más tarde.',
  };

  // Simulate API fetch - Replace with real API call later
  useEffect(() => {
    const fetchGroupBuys = async () => {
      try {
        setLoading(true);
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 500));

        // TODO: Replace with actual API call
        // const response = await fetch('/api/homepage/group-buys/active');
        // const data = await response.json();
        // setItems(data);

        // Use mock data for now
        setItems(MOCK_GROUP_BUYS);
        setError(null);
      } catch {
        setError('Failed to fetch group buys');
      } finally {
        setLoading(false);
      }
    };

    fetchGroupBuys();
  }, []);

  const lang = language as 'zh' | 'en' | 'es';

  // Don't render section if no items and not loading (optional: always show section)
  // if (!loading && items.length === 0) return null;

  return (
    <section className="py-16 bg-gradient-to-b from-orange-50 to-white" id="group-buy">
      <div className="container mx-auto px-4 md:px-6">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-block px-4 py-1.5 rounded-full bg-orange-100 text-orange-700 text-sm font-semibold mb-4">
            🛒 LIMITED TIME
          </div>
          <h2 className="text-3xl md:text-4xl font-bold text-gray-800 mb-4">
            {sectionTitle[lang]} <span className="text-orange-500">(+1)</span>
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            {sectionSubtitle[lang]}
          </p>
        </div>

        {/* Content */}
        {loading ? (
          // Loading State
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <GroupBuyCardSkeleton />
            <GroupBuyCardSkeleton />
          </div>
        ) : error ? (
          // Error State
          <div className="text-center py-12">
            <div className="text-red-500 text-lg mb-4">⚠️ {errorText[lang]}</div>
            <button
              onClick={() => window.location.reload()}
              className="text-orange-600 hover:text-orange-700 underline"
            >
              Retry
            </button>
          </div>
        ) : items.length === 0 ? (
          // Empty State
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🍍</div>
            <p className="text-gray-500 text-lg">{emptyText[lang]}</p>
          </div>
        ) : (
          // Items Grid
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {items.map((item) => (
              <GroupBuyCard key={item.id} item={item} language={language} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
