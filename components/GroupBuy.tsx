'use client';

import React from 'react';

export default function GroupBuy() {
  return (
    <section className="py-12 bg-orange-50" id="group-buy">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold text-orange-800 mb-6">Taiwanway 團購專區 (+1)</h2>
        <p className="text-gray-600 mb-8">在這裡預訂您最喜愛的台灣家鄉味！填寫下方表單即可完成預約。</p>
        
        <div className="bg-white p-8 rounded-2xl shadow-xl border border-orange-100">
          {/* 這裡可以嵌入 Google Form 或自定義表單 */}
          <iframe 
            src="https://docs.google.com/forms/d/e/1FAIpQLSc_YOUR_FORM_ID/viewform?embedded=true" 
            width="100%" 
            height="800" 
            frameBorder="0" 
            marginHeight={0} 
            marginWidth={0}
          >載入中…</iframe>
        </div>
        
        <div className="mt-8 text-sm text-gray-500">
          * 訂單將同步至 Google Sheets 進行處理
        </div>
      </div>
    </section>
  );
}
