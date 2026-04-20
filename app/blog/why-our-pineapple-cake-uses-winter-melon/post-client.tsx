'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'
import { getPostBySlug } from '../posts'

const SLUG = 'why-our-pineapple-cake-uses-winter-melon'

export function PineappleCakePostClient() {
  const { language } = useLanguage()
  const post = getPostBySlug(SLUG)!

  const backLabel =
    language === 'zh' ? '← 返回部落格' : language === 'es' ? '← Volver al blog' : '← Back to blog'
  const minutesLabel =
    language === 'zh'
      ? `${post.readingMinutes} 分鐘閱讀`
      : language === 'es'
        ? `${post.readingMinutes} min de lectura`
        : `${post.readingMinutes} min read`

  return (
    <main className="min-h-screen bg-cream pt-28 pb-20">
      <div className="mx-auto max-w-2xl px-4">
        <nav aria-label="Breadcrumb" className="mb-6 text-sm text-muted-foreground">
          <ol className="flex items-center gap-2 flex-wrap">
            <li>
              <Link href="/" className="hover:text-terracotta">
                {language === 'zh' ? '首頁' : language === 'es' ? 'Inicio' : 'Home'}
              </Link>
            </li>
            <li aria-hidden>/</li>
            <li>
              <Link href="/blog" className="hover:text-terracotta">
                Blog
              </Link>
            </li>
            <li aria-hidden>/</li>
            <li aria-current="page" className="text-foreground font-medium truncate">
              {language === 'zh' ? '鳳梨酥內餡' : language === 'es' ? 'Pastel de Piña' : 'Pineapple Cake'}
            </li>
          </ol>
        </nav>

        <article>
          <header className="mb-8">
            <div className="mb-3 flex items-center gap-3 text-xs text-muted-foreground">
              <time dateTime={post.date}>{post.date}</time>
              <span aria-hidden>·</span>
              <span>{minutesLabel}</span>
            </div>
            <h1 className="font-body text-3xl md:text-4xl font-bold text-foreground leading-tight tracking-tight mb-5">
              {post.title[language] || post.title.en}
            </h1>
            <div className="relative aspect-[16/10] w-full overflow-hidden rounded-2xl bg-sand/30 shadow-sm">
              <Image
                src={post.coverImage}
                alt="Taiwanese pineapple cake (鳳梨酥) cut open to show native pineapple and winter melon filling"
                fill
                priority
                className="object-cover"
                sizes="(min-width: 768px) 640px, 100vw"
              />
            </div>
          </header>

          <div className="font-body space-y-5 text-base md:text-[1.0625rem] leading-relaxed text-foreground/85">
            {language === 'zh' && <PostBodyZh />}
            {language === 'en' && <PostBodyEn />}
            {language === 'es' && <PostBodyEs />}
          </div>

          <footer className="mt-12 rounded-xl bg-sand/30 px-6 py-6 text-center">
            <p className="font-body text-foreground/90 mb-3">
              {language === 'zh'
                ? '想試一顆台灣空運土鳳梨冬瓜餡的鳳梨酥？'
                : language === 'es'
                  ? '¿Quieres probar un pastel de piña con relleno taiwanés auténtico?'
                  : 'Want to try one with the real Taiwan-imported filling?'}
            </p>
            <p className="font-body text-sm text-muted-foreground mb-4">
              TaiwanWay · 26 South St, Middletown, NY 10940 ·{' '}
              {language === 'zh'
                ? '週一、二、五、六 11AM–7PM'
                : language === 'es'
                  ? 'Lun / Mar / Vie / Sáb 11AM–7PM'
                  : 'Mon / Tue / Fri / Sat 11AM–7PM'}
            </p>
            <Link
              href="/blog"
              className="inline-flex items-center gap-1.5 text-sm font-semibold text-terracotta hover:underline"
            >
              {backLabel}
            </Link>
          </footer>
        </article>
      </div>
    </main>
  )
}

/* =====================================================================
 * 中文版
 * ===================================================================== */
function PostBodyZh() {
  return (
    <>
      <p>
        在美國，很多地方都能買到「pineapple cake」這三個字的點心，但大多數用的是濃縮鳳梨醬、玉米糖漿、加香精——做出來偏黃偏甜、口感黏膩，跟台灣街邊麵包店那一口酥脆、果香微酸的鳳梨酥，根本是兩種東西。
      </p>
      <p>
        TaiwanWay 的鳳梨酥只做一種——<strong>用台灣空運的土鳳梨，搭配古法冬瓜餡</strong>。為什麼這麼搞工？因為這才是「真的」台灣鳳梨酥該有的味道。
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        土鳳梨 vs 金鑽鳳梨：一字之差，風味天差地遠
      </h2>
      <p>走進台灣任何一家水果攤，會看到兩種鳳梨：</p>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          <strong>金鑽鳳梨</strong>：皮薄、汁多、果肉黃、甜度高，適合直接吃、打果汁——但做鳳梨酥<em>太水、太甜、香氣淡</em>
        </li>
        <li>
          <strong>土鳳梨</strong>（又叫「開英種」、「二號仔」）：皮厚、纖維粗、酸度明顯、香氣濃——做成鳳梨酥內餡，酸香才夠、不會死甜
        </li>
      </ul>
      <p>
        台灣做鳳梨酥的名店——微熱山丘、佳德、舊振南——<strong>全部使用土鳳梨</strong>。這不是行銷話術，是工藝選擇。TaiwanWay 的內餡也照這套規格走，我們從台灣南部契作土鳳梨園下單、熬煮成餡、空運到紐約。
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        冬瓜的角色：不是偷工，是講究
      </h2>
      <p>很多人第一次聽到「鳳梨酥加冬瓜」都會愣一下——「冬瓜？不是鳳梨酥嗎？」</p>
      <p>
        冬瓜餡在傳統鳳梨酥裡<strong>是主體</strong>，鳳梨餡才是點綴，比例大約<strong>冬瓜 70% + 鳳梨 30%</strong>。為什麼？
      </p>
      <ol className="list-decimal pl-6 space-y-2">
        <li><strong>平衡酸度</strong>——土鳳梨本身酸到會刮舌頭，不能單用</li>
        <li><strong>平衡甜度</strong>——純鳳梨餡熬到需要的質地，會過甜到蓋掉水果香</li>
        <li><strong>質地</strong>——冬瓜餡絞碎後帶有半透明膠質感，給鳳梨酥那獨特的 Q 彈口感</li>
        <li><strong>歷史傳統</strong>——鳳梨酥發源於台中、南投一帶的喜餅文化，冬瓜餡自古就是主角</li>
      </ol>
      <p>
        你在台灣吃到的<strong>任何老字號鳳梨酥，幾乎都是冬瓜鳳梨餡</strong>。純鳳梨餡是近十年興起的「土鳳梨酥」變種，強調果酸、鳳梨比例拉高到 50–60%——但冬瓜依然是基底。
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        為什麼要空運，不在美國生產？
      </h2>
      <p>我們在紐約開店，很多朋友建議：「美國也買得到鳳梨啊，買罐頭鳳梨打一打不就好？」</p>
      <p>
        短答：<strong>不行</strong>。理由：
      </p>
      <ul className="list-disc pl-6 space-y-2">
        <li><strong>土鳳梨美國幾乎買不到</strong>——美國超市的鳳梨 99% 是哥斯大黎加、菲律賓產的金鑽品種</li>
        <li><strong>罐頭鳳梨</strong>經過糖漬高溫殺菌，風味早已流失</li>
        <li><strong>冬瓜在美國華人超市有</strong>，但品質、水分不穩定</li>
        <li><strong>熬煮工藝</strong>需要純手工，從切、絞、熬到翻炒要 6–8 小時——台灣老店幾十年的經驗，不是看影片能複製的</li>
      </ul>
      <p>
        所以我們的做法是：<strong>餡料從台灣完成，空運到紐約</strong>。到店後才現烤酥皮、現包現做。每一顆鳳梨酥都是當天做的——在 Middletown 的 26 South St，你咬下去的是<strong>台灣當地的風土</strong>。
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        一顆 $3.25，你買到的不只是鳳梨酥
      </h2>
      <p>很多人覺得 $3.25 一顆貴。我們算過：</p>
      <ul className="list-disc pl-6 space-y-1">
        <li>台灣空運土鳳梨冬瓜餡的原料成本：約 $0.90</li>
        <li>純奶油酥皮：約 $0.50</li>
        <li>手工製作時間 + 烘烤：約 $0.40</li>
        <li>包裝 + 運營：約 $0.50</li>
        <li>合計：約 $2.30 成本</li>
      </ul>
      <p>
        但你買到的是：<strong>從台南鳳梨田到 Middletown 你手上、完整沒有打折的味道</strong>。
      </p>

      <p className="font-body text-lg font-semibold text-foreground mt-10 border-l-4 border-terracotta pl-4">
        如果你只在超市買過「pineapple cake」那種塑膠盒裝的點心，來 TaiwanWay 試一顆。咬下去的瞬間你會知道，這不是同一個東西。
      </p>
    </>
  )
}

/* =====================================================================
 * English version
 * ===================================================================== */
function PostBodyEn() {
  return (
    <>
      <p>
        In the US, &ldquo;pineapple cake&rdquo; shows up in Asian bakeries and supermarkets — but most are made with concentrated pineapple jam, corn syrup, and artificial flavoring. Bright yellow, overly sweet, sticky texture. That&apos;s not the pineapple cake Taiwanese people grew up with.
      </p>
      <p>
        At TaiwanWay, we make only one version — <strong>native Taiwanese pineapple air-freighted from Taiwan, combined with a traditional winter melon base</strong>. Here&apos;s why we go through all this trouble.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        Native Pineapple vs. Golden Pineapple: A World of Flavor Apart
      </h2>
      <p>Walk into any fruit market in Taiwan and you&apos;ll see two kinds of pineapple:</p>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          <strong>Golden (Jinzuan) pineapple</strong>: thin skin, juicy, sweet, bright yellow flesh — excellent fresh or in juice, but <em>too watery, too sweet, too mild</em> for baking
        </li>
        <li>
          <strong>Native pineapple</strong> (kāi-ing or &ldquo;No. 2&rdquo;): thick skin, coarser fibers, pronounced acidity, concentrated aroma — perfect for filling: tangy, fragrant, not cloying
        </li>
      </ul>
      <p>
        Taiwan&apos;s most revered pineapple cake bakeries — Sunnyhills, Chia Te, Kuo Yuan Ye — <strong>all use native pineapple</strong>. It&apos;s not marketing; it&apos;s craft. TaiwanWay sources from contract native-pineapple farms in southern Taiwan, cooks the filling on-site in Taiwan, and air-freights it to New York.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        The Role of Winter Melon: Not a Shortcut, a Tradition
      </h2>
      <p>
        When non-Taiwanese customers hear &ldquo;pineapple cake contains winter melon,&rdquo; they often do a double-take. &ldquo;Winter melon? I thought it was pineapple cake?&rdquo;
      </p>
      <p>
        <strong>Winter melon is the base of a traditional pineapple cake filling</strong>; pineapple is the accent — typically <strong>70% winter melon, 30% pineapple</strong>. Why?
      </p>
      <ol className="list-decimal pl-6 space-y-2">
        <li><strong>Balances acidity</strong> — native pineapple alone is tongue-tinglingly tart</li>
        <li><strong>Balances sweetness</strong> — pure pineapple cooked down becomes overpoweringly sweet</li>
        <li><strong>Provides texture</strong> — winter melon, minced and slow-cooked, gives that distinctive chewy-translucent quality</li>
        <li><strong>Historical tradition</strong> — pineapple cakes originated from wedding confections in central Taiwan, where winter melon filling has always been the foundation</li>
      </ol>
      <p>
        Any <strong>decades-old Taiwanese pineapple cake shop</strong> you walk into — the filling is winter melon + pineapple, not pure pineapple. The &ldquo;100% pineapple&rdquo; variety (<em>tǔ fènglí sū</em>) is a newer, tangier interpretation of the classic — but even those still use winter melon as the backbone.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        Why Airfreight, Why Not Make It Here?
      </h2>
      <p>
        Friends ask: &ldquo;You&apos;re in New York — just buy American pineapple, make the filling here, done.&rdquo;
      </p>
      <p>Short answer: <strong>no, because</strong>:</p>
      <ul className="list-disc pl-6 space-y-2">
        <li><strong>Native Taiwanese pineapple is essentially unavailable in the US</strong> — 99% of American supermarket pineapple is the golden variety from Costa Rica or the Philippines</li>
        <li><strong>Canned pineapple</strong> has been heat-sterilized and sugar-soaked; the flavor is long gone</li>
        <li><strong>Winter melon</strong> is available at Chinese grocers, but quality and water content varies wildly</li>
        <li><strong>The cooking technique</strong> — from peeling to mincing to slow-stirring over low heat — takes 6–8 hours of continuous attention. Decades of Taiwanese bakery knowledge doesn&apos;t transfer via YouTube tutorials.</li>
      </ul>
      <p>
        Our solution: <strong>filling made in Taiwan by experienced artisans, then air-freighted to New York</strong>. At the shop, we handcraft the butter pastry fresh daily and fill each cake by hand. Every pineapple cake on our counter was baked today — and what you bite into is <strong>the actual soil and climate of southern Taiwan</strong>, unchanged.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        $3.25 a Piece — Here&apos;s What That Buys
      </h2>
      <p>Some customers find $3.25 expensive. Breaking it down:</p>
      <ul className="list-disc pl-6 space-y-1">
        <li>Taiwan-imported native pineapple + winter melon filling: ~$0.90</li>
        <li>Pure butter pastry: ~$0.50</li>
        <li>Hand-shaping and baking time: ~$0.40</li>
        <li>Packaging + overhead: ~$0.50</li>
        <li>Subtotal cost: ~$2.30</li>
      </ul>
      <p>
        But what you&apos;re buying is: <strong>the actual flavor of a Tainan pineapple farm, delivered complete and undiluted to Middletown, NY</strong>.
      </p>

      <p className="font-body text-lg font-semibold text-foreground mt-10 border-l-4 border-terracotta pl-4">
        If you&apos;ve only had the plastic-tray &ldquo;pineapple cake&rdquo; from supermarket aisles, come try one at TaiwanWay. The moment you bite in, you&apos;ll know — these are not the same thing.
      </p>
    </>
  )
}

/* =====================================================================
 * Spanish version
 * ===================================================================== */
function PostBodyEs() {
  return (
    <>
      <p>
        En Estados Unidos, &ldquo;pineapple cake&rdquo; aparece en panaderías asiáticas y supermercados — pero la mayoría se hacen con mermelada de piña concentrada, jarabe de maíz y aromatizantes artificiales. Color demasiado amarillo, sabor excesivamente dulce, textura pegajosa. No es el pastel de piña con el que creció la gente de Taiwán.
      </p>
      <p>
        En TaiwanWay solo hacemos una versión — <strong>piña nativa taiwanesa enviada por aire desde Taiwán, combinada con relleno tradicional de melón de invierno</strong>. He aquí por qué nos tomamos esta molestia.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        Piña Nativa vs. Piña Dorada: Un Mundo de Diferencia
      </h2>
      <p>Si entras a cualquier frutería en Taiwán, verás dos tipos de piña:</p>
      <ul className="list-disc pl-6 space-y-2">
        <li>
          <strong>Piña dorada (Jinzuan)</strong>: piel delgada, jugosa, dulce, carne amarilla brillante — excelente fresca o en jugo, pero <em>demasiado acuosa, demasiado dulce, demasiado suave</em> para hornear
        </li>
        <li>
          <strong>Piña nativa</strong> (kāi-ing o &ldquo;No. 2&rdquo;): piel gruesa, fibras más gruesas, acidez pronunciada, aroma concentrado — perfecta para relleno: ácida, fragante, no empalagosa
        </li>
      </ul>
      <p>
        Las panaderías de pastel de piña más reverenciadas de Taiwán — Sunnyhills, Chia Te, Kuo Yuan Ye — <strong>todas usan piña nativa</strong>. No es marketing; es oficio. TaiwanWay se abastece de granjas de piña nativa por contrato en el sur de Taiwán, cocina el relleno in situ en Taiwán, y lo envía por aire a Nueva York.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        El Papel del Melón de Invierno: No Un Atajo, Una Tradición
      </h2>
      <p>
        Cuando clientes no-taiwaneses oyen &ldquo;el pastel de piña contiene melón de invierno,&rdquo; suelen sorprenderse. &ldquo;¿Melón de invierno? ¿No era pastel de piña?&rdquo;
      </p>
      <p>
        <strong>El melón de invierno es la base del relleno tradicional</strong>; la piña es el acento — típicamente <strong>70% melón de invierno, 30% piña</strong>. ¿Por qué?
      </p>
      <ol className="list-decimal pl-6 space-y-2">
        <li><strong>Equilibra la acidez</strong> — la piña nativa sola es agresivamente ácida</li>
        <li><strong>Equilibra el dulzor</strong> — la piña pura cocida a fuego lento se vuelve abrumadoramente dulce</li>
        <li><strong>Aporta textura</strong> — el melón de invierno, picado y cocido lentamente, da esa calidad masticable-translúcida distintiva</li>
        <li><strong>Tradición histórica</strong> — el pastel de piña surgió de la confitería de bodas en el centro de Taiwán, donde el relleno de melón de invierno siempre ha sido la base</li>
      </ol>
      <p>
        Cualquier <strong>panadería taiwanesa de décadas de tradición</strong> que visites — el relleno es melón de invierno + piña, no piña pura. La variedad &ldquo;100% piña&rdquo; (<em>tǔ fènglí sū</em>) es una interpretación más nueva y ácida del clásico — pero incluso esas siguen usando melón de invierno como columna vertebral.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        ¿Por Qué Traer por Aire, No Hacerlo Aquí?
      </h2>
      <p>
        Los amigos preguntan: &ldquo;Estáis en Nueva York — comprad piña americana, haced el relleno aquí, fin.&rdquo;
      </p>
      <p>Respuesta corta: <strong>no, porque</strong>:</p>
      <ul className="list-disc pl-6 space-y-2">
        <li><strong>La piña nativa taiwanesa es prácticamente inencontrable en EE.UU.</strong> — el 99% de la piña de supermercado americano es la variedad dorada de Costa Rica o Filipinas</li>
        <li><strong>La piña enlatada</strong> ha sido esterilizada y remojada en azúcar; el sabor se ha perdido hace tiempo</li>
        <li><strong>El melón de invierno</strong> se encuentra en mercados chinos, pero la calidad y el contenido de agua varían mucho</li>
        <li><strong>La técnica de cocción</strong> — de pelar a picar a revolver lentamente a fuego bajo — requiere 6–8 horas de atención continua. Décadas de conocimiento de panadería taiwanesa no se transfieren por tutoriales de YouTube.</li>
      </ul>
      <p>
        Nuestra solución: <strong>relleno hecho en Taiwán por artesanos experimentados, luego enviado por aire a Nueva York</strong>. En la tienda, elaboramos la masa de mantequilla a mano cada día y rellenamos cada pastel manualmente. Cada pastel de piña en nuestra barra se horneó hoy — y lo que muerdes es <strong>el suelo y el clima reales del sur de Taiwán</strong>, sin alteración.
      </p>

      <h2 className="font-body text-2xl font-bold text-foreground mt-10 mb-4">
        $3.25 la Pieza — Esto Es Lo Que Compras
      </h2>
      <p>Algunos clientes piensan que $3.25 es caro. Desglose:</p>
      <ul className="list-disc pl-6 space-y-1">
        <li>Relleno de piña nativa + melón de invierno importado de Taiwán: ~$0.90</li>
        <li>Masa de mantequilla pura: ~$0.50</li>
        <li>Tiempo de moldeado a mano y horneado: ~$0.40</li>
        <li>Empaquetado + gastos generales: ~$0.50</li>
        <li>Subtotal de costos: ~$2.30</li>
      </ul>
      <p>
        Pero lo que compras es: <strong>el sabor real de una granja de piña de Tainan, entregado completo y sin diluir a Middletown, NY</strong>.
      </p>

      <p className="font-body text-lg font-semibold text-foreground mt-10 border-l-4 border-terracotta pl-4">
        Si solo has probado el &ldquo;pineapple cake&rdquo; de bandeja de plástico de los pasillos de supermercado, ven a probar uno en TaiwanWay. En el momento que muerdes, lo sabrás — no son la misma cosa.
      </p>
    </>
  )
}
