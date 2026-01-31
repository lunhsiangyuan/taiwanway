'use client';

import React from 'react';

export function GroupBuy() {
  return (
    <section className="py-12 bg-orange-50" id="group-buy">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <div className="inline-block px-4 py-1 rounded-full bg-orange-200 text-orange-800 text-sm font-bold mb-4">
          LIMITED TIME OFFER
        </div>
        <h2 className="text-3xl font-bold text-orange-800 mb-6">Taiwanway 團購專區 (+1)</h2>
        <p className="text-gray-600 mb-8">在這裡預訂您最喜愛的台灣家鄉味！填寫下方表單即可完成預約。</p>
        
        <div className="bg-white p-4 rounded-2xl shadow-xl border border-orange-100 min-h-[400px]">
          <iframe 
            src="https://docs.google.com/forms/d/e/1FAIpQLSc_YOUR_FORM_ID/viewform?embedded=true" 
            width="100%" 
            height="600" 
            className="rounded-lg"
          >載入中…</iframe>
        </div>
      </div>
    </section>
  );
}
