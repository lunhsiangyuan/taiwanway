'use client'

import { ChevronDown, Truck } from 'lucide-react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/i18n/language-context'
import { cn } from '@/lib/utils'

export const UBER_URL = 'https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A'
export const DOORDASH_URL = 'https://www.doordash.com/store/taiwan-way-middletown-42843267/'

/**
 * 外送平台開關 —— 2026-08-27 起暫停 Uber Eats，全站只保留 DoorDash。
 * 要恢復 Uber Eats：把這個常數改回 true，Header／訂餐按鈕／產品卡片會一起恢復。
 * （json-ld.tsx 的 sameAs 與 app/faq/faqs.ts 的外送問答需另外手動改回）
 */
export const UBER_ENABLED = false

type OrderButtonProps = {
  className?: string
  fullWidth?: boolean
  showIcon?: boolean
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'bottom'
}

/**
 * 共用「線上訂餐」按鈕 — 單顆磚紅品牌色。
 * UBER_ENABLED 為 true 時展開 Uber Eats / DoorDash 下拉；
 * 為 false 時（目前狀態）只剩 DoorDash，直接連出去不再顯示下拉。
 * 全站（Header／菜單／聯絡）統一使用，確保視覺一致。
 */
export function OrderButton({
  className,
  fullWidth = false,
  showIcon = true,
  align = 'center',
  side = 'bottom',
}: OrderButtonProps) {
  const { language } = useLanguage()
  const label = language === 'zh' ? '線上訂餐' : language === 'es' ? 'Pedir en línea' : 'Order Online'

  // 只剩 DoorDash 一個平台，不需要下拉選單，直接連出去
  if (!UBER_ENABLED) {
    return (
      <Button
        asChild
        className={cn(
          'bg-primary text-primary-foreground hover:bg-accent font-body font-semibold rounded-full flex items-center justify-center gap-1.5',
          fullWidth && 'w-full',
          className
        )}
      >
        <a href={DOORDASH_URL} target="_blank" rel="noopener noreferrer">
          {showIcon && <Truck className="h-4 w-4" />}
          {label}
        </a>
      </Button>
    )
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          className={cn(
            'bg-primary text-primary-foreground hover:bg-accent font-body font-semibold rounded-full flex items-center justify-center gap-1.5',
            fullWidth && 'w-full',
            className
          )}
        >
          {showIcon && <Truck className="h-4 w-4" />}
          {label}
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align={align} side={side} className="min-w-[11rem]">
        <DropdownMenuItem asChild className="cursor-pointer font-body font-medium">
          <a href={UBER_URL} target="_blank" rel="noopener noreferrer">
            <span className="mr-2 text-[#06C167]">●</span> Uber Eats
          </a>
        </DropdownMenuItem>
        <DropdownMenuItem asChild className="cursor-pointer font-body font-medium">
          <a href={DOORDASH_URL} target="_blank" rel="noopener noreferrer">
            <span className="mr-2 text-[#FF3008]">●</span> DoorDash
          </a>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
