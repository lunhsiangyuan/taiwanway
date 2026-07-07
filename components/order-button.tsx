'use client'

import { ChevronDown, Truck } from 'lucide-react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/i18n/language-context'
import { cn } from '@/lib/utils'

export const UBER_URL = 'https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A'
export const DOORDASH_URL = 'https://www.doordash.com/store/taiwan-way-middletown-42843267/'

type OrderButtonProps = {
  className?: string
  fullWidth?: boolean
  showIcon?: boolean
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'bottom'
}

/**
 * 共用「線上訂餐」按鈕 — 單顆磚紅品牌色，點開展開 Uber Eats / DoorDash。
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
