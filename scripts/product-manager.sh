#!/bin/bash
# 台灣味產品管理工具 — 供 OpenClaw Agents 使用
# 密碼從環境變數讀取，不硬編碼
#
# 用法：
#   product-manager.sh upload <image_path>          — 上傳圖片，回傳 URL
#   product-manager.sh stage <json_file>            — 建立 staged 產品（is_active=false）
#   product-manager.sh stage-inline '<json>'        — 直接傳 JSON 建立 staged 產品
#   product-manager.sh create <json_file>           — 建立產品（is_active=true）
#   product-manager.sh create-inline '<json>'       — 直接傳 JSON 建立產品
#   product-manager.sh list                         — 列出所有產品
#   product-manager.sh list-staged                  — 列出待上架產品
#   product-manager.sh activate-all                 — 上架所有 staged 產品
#   product-manager.sh qr <slug>                    — 下載單個 QR Code PNG
#   product-manager.sh qr-batch [output_dir]        — 批次下載所有 active 產品 QR Code
#   product-manager.sh delete <id>                  — 停用產品

API="https://taiwanwayny.com/api/products"
PW="${TAIWANWAY_ADMIN_PW:?請設定 TAIWANWAY_ADMIN_PW 環境變數}"

auth_header() {
  echo "x-admin-password: ${PW}"
}

case "$1" in
  upload)
    [ -z "$2" ] && { echo "用法: product-manager.sh upload <image_path>"; exit 1; }
    curl -s -X POST "${API}/upload" \
      -H "$(auth_header)" \
      -F "file=@$2"
    ;;

  stage)
    [ -z "$2" ] && { echo "用法: product-manager.sh stage <json_file>"; exit 1; }
    # Inject is_active=false into the JSON
    JSON=$(python3 -c "import json,sys; d=json.load(open(sys.argv[1])); d['is_active']=False; print(json.dumps(d))" "$2")
    curl -s -X POST "${API}" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d "${JSON}"
    ;;

  stage-inline)
    [ -z "$2" ] && { echo "用法: product-manager.sh stage-inline '<json>'"; exit 1; }
    JSON=$(python3 -c "import json,sys; d=json.loads(sys.argv[1]); d['is_active']=False; print(json.dumps(d))" "$2")
    curl -s -X POST "${API}" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d "${JSON}"
    ;;

  create)
    [ -z "$2" ] && { echo "用法: product-manager.sh create <json_file>"; exit 1; }
    curl -s -X POST "${API}" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d @"$2"
    ;;

  create-inline)
    [ -z "$2" ] && { echo "用法: product-manager.sh create-inline '<json>'"; exit 1; }
    curl -s -X POST "${API}" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d "$2"
    ;;

  list)
    curl -s "${API}" -H "$(auth_header)" | python3 -m json.tool
    ;;

  list-staged)
    curl -s "${API}" -H "$(auth_header)" | \
      python3 -c "import json,sys; [print(json.dumps(p,ensure_ascii=False)) for p in json.load(sys.stdin) if not p.get('is_active')]"
    ;;

  activate-all)
    echo "正在上架所有 staged 產品..."
    RESULT=$(curl -s -X POST "${API}/activate" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d '{}')
    echo "${RESULT}" | python3 -m json.tool
    ;;

  qr)
    [ -z "$2" ] && { echo "用法: product-manager.sh qr <slug>"; exit 1; }
    OUTFILE="${3:-qr-${2}.png}"
    curl -s "${API}/qr?slug=$2" -o "${OUTFILE}"
    echo "QR Code 已存到 ${OUTFILE}"
    ;;

  qr-batch)
    OUTDIR="${2:-./qr-codes}"
    mkdir -p "${OUTDIR}"
    echo "批次下載 QR Code 到 ${OUTDIR}/"
    SLUGS=$(curl -s "${API}" -H "$(auth_header)" | \
      python3 -c "import json,sys; [print(p['slug']) for p in json.load(sys.stdin) if p.get('is_active')]")
    COUNT=0
    for SLUG in ${SLUGS}; do
      curl -s "${API}/qr?slug=${SLUG}" -o "${OUTDIR}/qr-${SLUG}.png"
      echo "  ✓ ${SLUG}"
      COUNT=$((COUNT+1))
    done
    echo "完成！共 ${COUNT} 個 QR Code"
    ;;

  delete)
    [ -z "$2" ] && { echo "用法: product-manager.sh delete <product_id>"; exit 1; }
    curl -s -X DELETE "${API}" \
      -H "$(auth_header)" \
      -H "Content-Type: application/json" \
      -d "{\"id\":\"$2\"}"
    ;;

  *)
    cat <<'HELP'
台灣味產品管理工具（芺利蓮專用）

指令：
  upload <image_path>          上傳圖片，回傳 URL
  stage <json_file>            建立 staged 產品（不上架）
  stage-inline '<json>'        直接傳 JSON 建立 staged 產品
  create <json_file>           建立產品（直接上架）
  create-inline '<json>'       直接傳 JSON 建立產品
  list                         列出所有產品
  list-staged                  列出待上架產品
  activate-all                 上架所有 staged 產品
  qr <slug> [output.png]       下載單個 QR Code PNG
  qr-batch [output_dir]        批次下載所有 active 產品 QR Code
  delete <product_id>          停用產品

環境變數：
  TAIWANWAY_ADMIN_PW           必要，管理員密碼
HELP
    ;;
esac
