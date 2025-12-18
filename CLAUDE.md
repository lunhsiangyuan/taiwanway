# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Multi-Agent Revenue Analysis System** for analyzing Taiwanway restaurant payment data from Square API. The system uses an Orchestrator-Subagent architecture with specialized AI agents for sales analysis, customer behavior analysis, and financial metrics analysis.

**Key Technologies**: Python, pandas, matplotlib/seaborn, pytz, YAML configuration

---

## Claude Agent SDK 整合

本專案已完整遷移至 Claude Agent SDK 架構，使用 Subagent 模式進行分析任務的分工和協調。

### 新架構目錄結構

```
.claude/
├── agents/                          # Subagent 定義（Markdown）
│   ├── data-agent.md               # 數據載入與預處理
│   ├── sales-agent.md              # 銷售趨勢分析
│   ├── customer-agent.md           # 客戶行為分析
│   ├── financial-agent.md          # 財務指標分析
│   ├── report-agent.md             # 報告生成
│   ├── break-even/                 # 損益平衡子系統
│   │   ├── orchestrator.md         # 子系統協調器
│   │   ├── data-prep.md            # 數據準備
│   │   ├── calculation.md          # 損益平衡計算
│   │   ├── profit-target.md        # 利潤目標分析
│   │   ├── sensitivity.md          # 敏感度分析
│   │   ├── visualization.md        # 視覺化生成
│   │   └── report.md               # 報告生成
│   └── shared/                     # 共享配置
│       ├── business-rules.md       # 業務規則
│       └── data-conventions.md     # 數據慣例
└── commands/                        # Slash 命令
    ├── analyze.md                  # /analyze 完整分析
    ├── break-even.md               # /break-even 損益平衡
    └── report.md                   # /report 報告生成

tools/                               # MCP 工具（Python）
├── __init__.py
├── data_tools.py                   # 數據處理工具
├── analysis_tools.py               # 分析工具
├── memory_tools.py                 # 記憶系統工具
├── visualization_tools.py          # 視覺化工具
└── break_even_tools.py             # 損益平衡工具

agents/legacy/                       # 舊系統備份
```

### Slash 命令

使用以下命令執行分析任務：

| 命令 | 功能 | 範例 |
|------|------|------|
| `/analyze` | 完整營收分析 | `/analyze data/all_payments.csv` |
| `/break-even` | 損益平衡分析 | `/break-even --labor 160` |
| `/report` | 報告生成 | `/report full --format markdown` |

### Subagent 對應關係

| 舊 Python Agent | 新 Subagent | 工具檔案 |
|-----------------|-------------|----------|
| `data_agent.py` | `data-agent.md` | `data_tools.py` |
| `sales_analysis_agent.py` | `sales-agent.md` | `analysis_tools.py` |
| `customer_behavior_agent.py` | `customer-agent.md` | `analysis_tools.py` |
| `financial_agent.py` | `financial-agent.md` | `analysis_tools.py` |
| `report_agent.py` | `report-agent.md` | - |
| `break_even/*.py` (7 個) | `break-even/*.md` (7 個) | `break_even_tools.py` |

### MCP 工具清單

#### 數據工具 (data_tools.py)
- `load_square_data(file_path)` - 載入 Square 支付數據
- `validate_data(df)` - 驗證數據完整性
- `preprocess_data(df)` - 預處理（時區轉換、欄位計算）
- `filter_by_business_rules(df)` - 套用業務規則過濾
- `generate_data_summary(df)` - 生成數據摘要
- `export_to_csv(df, path)` - 匯出 CSV

#### 分析工具 (analysis_tools.py)
- `analyze_hourly_sales(df)` - 每小時營收分析
- `analyze_daily_sales(df)` - 每日營收分析
- `analyze_monthly_sales(df)` - 月度營收分析
- `analyze_customer_segments(df)` - 客戶分群
- `analyze_revenue_metrics(df)` - 營收指標
- `identify_peak_hours(df)` - 識別尖峰時段

#### 記憶工具 (memory_tools.py)
- `remember(key, content, tags)` - 記憶存儲
- `recall(key)` - 記憶回憶
- `search_by_tag(tag)` - 按標籤搜尋
- `get_experience(context)` - 獲取相關經驗
- `get_memory_summary()` - 記憶統計

#### 視覺化工具 (visualization_tools.py)
- `generate_hourly_chart(data)` - 每小時圖表
- `generate_monthly_chart(data)` - 月度圖表
- `generate_heatmap(data)` - 熱力圖
- `generate_category_chart(data)` - 類別圖表

#### 損益平衡工具 (break_even_tools.py)
- `calculate_break_even(params)` - 計算損益平衡點
- `sensitivity_analysis(params)` - 敏感度分析
- `profit_target_analysis(target)` - 利潤目標分析
- `scenario_comparison()` - 情境比較
- `generate_break_even_report()` - 生成報告

### 功能遷移說明

#### Sequential Thinking → Extended Thinking
原系統的 `ThinkingChain` 已遷移為每個 Subagent 的結構化思考流程：

```markdown
## 思考流程

### Step 1: 理解任務
- 分析輸入數據和目標

### Step 2: 規劃步驟
- 設計分析方法

### Step 3: 執行分析
- 調用工具執行

### Step 4: 驗證結果
- 檢查結果合理性

### Step 5: 總結洞察
- 提取關鍵發現
```

#### Memory 系統 → MCP 工具
原系統的 `AgentMemory` 已封裝為 MCP 工具：

```python
# 存儲分析結果
remember(
    key="analysis_2025_11",
    content={"revenue": 12000, "insights": [...]},
    tags=["monthly", "revenue"],
    importance="high"
)

# 回憶過往經驗
past = recall("analysis_2025_10")
experience = get_experience("revenue_analysis")
```

存儲位置：`agents/memory_store/`

#### 並行執行 → Task Tool
使用 Task Tool 實現並行委派：

```
使用 Task Tool 同時調用：
- sales-agent（銷售分析）
- customer-agent（客戶分析）
- financial-agent（財務分析）
```

### 舊系統備份

原 Python Multi-Agent 系統已備份至 `agents/legacy/`：
- `base_agent.py` - 基礎代理類
- `thinking.py` - Sequential Thinking 實現
- `memory.py` - 記憶系統實現
- `orchestrator.py` - 協調器
- `data_agent.py` - 數據代理
- `sales_analysis_agent.py` - 銷售分析
- `customer_behavior_agent.py` - 客戶分析
- `financial_agent.py` - 財務分析
- `report_agent.py` - 報告代理
- `break_even/` - 損益平衡子系統

### 回滾方法

如需恢復舊系統：
```bash
cp -r agents/legacy/* agents/
rm -rf .claude/agents/ .claude/commands/
```

---

## Common Development Commands

### Agent System (Primary Interface)

```bash
# Full analysis with all agents
python3 agents/orchestrator.py --task full_analysis --data data/items-2025-01-01-2025-11-16.csv

# Specific analyses
python3 agents/orchestrator.py --task sales_analysis --data <file>
python3 agents/orchestrator.py --task customer_analysis --data <file>
python3 agents/orchestrator.py --task financial_analysis --data <file>

# With date range filtering
python3 agents/orchestrator.py --task full_analysis --data <file> \
  --start-date 2025-09-01 --end-date 2025-09-30

# Run agent tests
python3 agents/test_agents.py
```

### Data Processing Pipeline

```bash
# 1. Download and merge Square API data
python3 scripts/download_all_payments_mcp.py

# 2. Convert JSON to CSV
python3 scripts/convert_mcp_json_to_csv.py data/all_payments/all_payments.json

# 3. Generate reports
python3 scripts/generate_html_report.py data/all_payments/all_payments.csv
python3 scripts/generate_monthly_report.py data/all_payments/all_payments.csv
python3 scripts/generate_data_report.py

# 4. Check download status
python3 scripts/show_status.py
```

### Analysis Scripts

```bash
# Hourly traffic and revenue analysis (main analysis script)
python3 scripts/analysis/analyze_hourly_traffic.py

# Other analyses
python3 scripts/analysis/analyze_weekday_revenue.py
python3 scripts/analysis/calculate_total_revenue.py
python3 scripts/analysis/create_hourly_revenue_heatmap.py
python3 scripts/analysis/create_hourly_revenue_heatmap.py
python3 scripts/analysis/analyze_cost_structure.py

# Q4 2025 Analysis (Sep-Nov)
python3 scripts/analyze_november_revenue.py
python3 scripts/analyze_fall_revenue.py
python3 scripts/generate_pdf_report.py

# Break-even analysis (損益平衡分析)
python3 scripts/analysis/analyze_break_even_q4.py
```

### Dependencies

```bash
pip install pandas matplotlib seaborn scienceplots pytz pyyaml
```

## System Architecture

### Multi-Agent Architecture

The system follows an **Orchestrator-Subagent Pattern**:

```
OrchestratorAgent (orchestrator.py)
├── DataAgent (data_agent.py)           # Loads, validates, preprocesses data
├── SalesAnalysisAgent                  # Hourly/daily/monthly sales trends
├── CustomerBehaviorAgent               # Segmentation, preferences, patterns
├── FinancialAgent                      # Revenue metrics, AOV, tax analysis
└── ReportAgent (report_agent.py)       # Generates JSON/Markdown/CSV reports
```

**Key Pattern**: All agents inherit from `BaseAgent` abstract class which provides:
- Standardized `execute()`, `validate_input()`, and `run()` methods
- Error handling and status tracking (initialized → running → completed/failed)
- Execution timing and metadata collection
- Structured logging

### Data Flow Pipeline

```
Square API (Payments)
  ↓ (MCP scripts download)
JSON files → download_all_payments_mcp.py → all_payments.json
  ↓ (conversion)
CSV file → all_payments.csv
  ↓ (DataAgent preprocessing)
Clean DataFrame
  ↓ (passed to all analysis agents in parallel)
[SalesAgent, CustomerAgent, FinancialAgent] → results
  ↓ (ReportAgent aggregation)
Output: JSON reports, Markdown summaries, CSV exports
```

### Configuration System

**Location**: `agents/config.yaml`

The system is configuration-driven with sections for:
- `global`: timezone (America/New_York), output directories
- `data_agent`: caching, validation, preprocessing settings
- `sales_agent`: analysis types, top N products, growth calculations
- `customer_agent`: segmentation thresholds (VIP/Regular), analysis types
- `financial_agent`: metrics to calculate, Pareto analysis settings
- `report_agent`: output formats (json/markdown/csv), recommendations
- `business_rules`: operating days [0,1,4,5], hours [10-20], closed months [6,7]
- `performance`: parallel execution, batch size

**Important**: Modify `config.yaml` to change analysis behavior without code changes.

### Output Structure

```
agents/output/
├── reports/
│   ├── full_analysis_report_<timestamp>.json     # Complete data dump
│   └── full_analysis_summary_<timestamp>.md      # Executive summary
├── data/
│   ├── hourly_sales_<timestamp>.csv
│   └── monthly_sales_<timestamp>.csv
└── results/
    └── orchestrator_results_<timestamp>.json

analysis_output/
├── data/
│   ├── hourly/          # Hourly analysis JSON/CSV
│   └── weekday/         # Weekday revenue JSON/CSV
├── charts/
│   ├── hourly/          # PNG charts for hourly traffic/revenue
│   └── weekday/         # PNG charts for weekday analysis
└── break_even_q4/       # Q4 2025 損益平衡分析
    ├── README.md                     # 分析說明文件
    ├── break_even_report.md          # 完整分析報告
    ├── data/
    │   └── monthly_stats.csv         # 月度統計數據
    └── charts/
        ├── break_even_analysis.png       # 損益平衡點分析
        ├── break_even_days.png           # 三種日營收情境損益平衡天數 (4×3)
        ├── cost_breakdown.png            # 成本結構分解圖
        ├── labor_sensitivity_table.png   # 人力成本敏感度表
        ├── monthly_pnl_comparison.png    # 月度損益比較
        ├── sensitivity_3d_heatmap.png    # 三維敏感度熱力圖 (2×2)
        └── sensitivity_heatmap.png       # 基本敏感度熱力圖
```

## Critical Business Rules

### Operating Schedule
- **Operating Days**: Monday (0), Tuesday (1), Friday (4), Saturday (5)
- **Operating Hours**: 10:00-20:00
- **Closed Months**: June (6), July (7) - summer break
- **Special Holidays**: Christmas (12-25)

### Timezone Handling
- **Source**: UTC from Square API
- **Target**: America/New_York with automatic DST handling via pytz
- **DST Periods**:
  - EDT (UTC-4): March 2nd Sunday → November 1st Sunday
  - EST (UTC-5): November 1st Sunday → March 2nd Sunday
- **Critical**: Always use `pytz.timezone('America/New_York')` instead of fixed UTC offsets

### Data Processing Rules
- Only process transactions with `status == "COMPLETED"`
- Deduplicate by payment ID
- Filter by operating days and months
- Monetary values: convert from cents (÷100) to dollars
- Revenue calculation uses "daily average per hour" (total revenue for hour / days that hour appears)

### Square API Integration
- **Location ID**: `LMDN6Z5DKNJ2P`
- **Pagination**: Cursor-based, 100 records per page
- **Date Range**: Filters to 2025-01-01 onwards (current focus period)
- **MCP Tool**: Square MCP server handles actual API calls

### Cost Parameters (損益平衡分析)
- **Fixed Costs**: $3,800/month (Rent $3,100 + Utilities $700)
- **Labor Costs**: $100, $160, $200, $250/day (four scenarios)
- **Food Cost Rates**: 30%, 35%, 40% (three scenarios)
- **NYC Sales Tax**: 8.875% (NY State 4% + NYC 4.5% + MTA 0.375%)
- **Break-even Formula**: `Revenue = (Fixed + Labor) / (1 - Food Cost Rate)`
- **Daily Revenue Scenarios**:
  - 淡季 $640 (November actual)
  - 平均 $753 (Q4 average)
  - 旺季 $820 (September actual)

### Revenue Calculation (營收計算)
- **Data Source**: Payments CSV from Square MCP (`payments_2025_XX.csv`)
- **Filter**: Only `status == 'COMPLETED'` transactions (exclude FAILED, CANCELED)
- **Net Sales**: `amount / (1 + 0.08875)` - convert from gross (tax-inclusive) to net (tax-exclusive)
- **Validation**: Results match Square Summary Report within 1%

## Code Architecture Details

### Agent Lifecycle

Every agent follows this execution pattern:

```python
agent = SpecificAgent(config)
result = agent.run(data, params)  # Returns structured dict

# Internally:
# 1. validate_input(data) - Check data validity
# 2. execute(data, params) - Perform analysis
# 3. Update status and metadata
# 4. Return {"agent_id": ..., "status": ..., "results": ..., "metadata": ...}
```

### Adding a New Agent

1. Create new file in `agents/` directory
2. Inherit from `BaseAgent`
3. Implement `validate_input()` and `execute()` methods
4. Add configuration section to `config.yaml`
5. Register in `orchestrator.py` subagents dictionary
6. Agent will automatically integrate into the pipeline

### Error Handling Strategy

- **Input Validation**: Each agent validates before execution
- **Try-Catch Wrapping**: All executions wrapped in error handlers
- **Graceful Degradation**: System continues even if individual agents fail
- **Status Tracking**: Every agent reports state transitions
- **Metadata Preservation**: Error messages stored in `metadata["errors"]`

### Performance Characteristics

For ~9,000 records:
- DataAgent: ~0.09s (load, parse, validate, transform)
- SalesAgent: ~0.02s (7 different analyses)
- CustomerAgent: ~0.04s (6 different analyses)
- FinancialAgent: ~0.01s (6 different analyses)
- **Total**: ~0.16s for complete analysis

## Chinese Text Visualization

### Font Handling

All matplotlib charts require explicit Chinese font configuration:

```python
# MUST disable LaTeX rendering
plt.rcParams['text.usetex'] = False

# Load Chinese font (macOS paths)
chinese_font_paths = [
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
]

# Apply to all text elements
ax.set_title('標題', fontproperties=chinese_font_prop)
ax.set_xlabel('X軸', fontproperties=chinese_font_prop)
```

If fonts don't display correctly:
```bash
rm -rf ~/.matplotlib/fontlist-*.json  # Clear font cache
```

## Data Processing Patterns

### Loading Square Payment Data

```python
# Pattern used in DataAgent
df = pd.read_csv(file_path)

# Parse monetary columns (handles "$15.50" → 15.50)
df['Net Sales'] = df['Net Sales'].replace('[\$,]', '', regex=True).astype(float)

# Parse and convert timezone
df['DateTime'] = pd.to_datetime(df['DateTime'], utc=True)
ny_tz = pytz.timezone('America/New_York')
df['DateTime'] = df['DateTime'].dt.tz_convert(ny_tz)

# Extract time components
df['Hour'] = df['DateTime'].dt.hour
df['DayOfWeek'] = df['DateTime'].dt.dayofweek
df['Month'] = df['DateTime'].dt.month
df['YearMonth'] = df['DateTime'].dt.to_period('M')
```

### Filtering by Business Rules

```python
# Filter operating days (Mon, Tue, Fri, Sat)
operating_days = [0, 1, 4, 5]
df = df[df['DayOfWeek'].isin(operating_days)]

# Filter operating months (exclude Jun, Jul)
closed_months = [6, 7]
df = df[~df['Month'].isin(closed_months)]

# Filter operating hours (10:00-20:00)
df = df[(df['Hour'] >= 10) & (df['Hour'] <= 20)]
```

### Hourly Revenue Calculation

```python
# Calculate daily average per hour (not simple sum)
hourly = df.groupby(['YearMonth', 'Hour']).agg({
    'Net Sales': 'sum',
    'DateTime': 'nunique'  # Count unique days
}).reset_index()

hourly['Avg Daily Revenue'] = hourly['Net Sales'] / hourly['DateTime']
```

## Key Files and Their Purposes

### Agent System
- `agents/base_agent.py` - Abstract base class for all agents
- `agents/orchestrator.py` - Main coordinator, CLI entry point
- `agents/data_agent.py` - Data loading and preprocessing
- `agents/config.yaml` - System-wide configuration

### Data Pipeline
- `scripts/download_all_payments_mcp.py` - Download & merge Square data
- `scripts/convert_mcp_json_to_csv.py` - JSON to CSV conversion
- `scripts/generate_html_report.py` - HTML report generation

### Analysis
- `scripts/analysis/analyze_hourly_traffic.py` - Main hourly analysis (traffic + revenue)
- `scripts/analysis/analyze_cost_structure.py` - Cost and profit analysis
- `scripts/analysis/analyze_break_even_q4.py` - Q4 2025 break-even analysis (損益平衡分析)

### Documentation
- `README.md` - Comprehensive project documentation (Chinese)
- `agents/README.md` - Agent system overview
- `agents/ARCHITECTURE.md` - Detailed architecture documentation
- `agents/QUICKSTART.md` - Quick start guide

## Development Guidelines

### When Modifying Analysis Logic

1. **Check config.yaml first** - Many behaviors are configurable
2. **Respect business rules** - Operating days/hours/months are critical
3. **Maintain timezone handling** - Always use pytz for DST correctness
4. **Test with actual data** - Use data/all_payments/all_payments.csv
5. **Update both agents and legacy scripts** - Some analyses exist in both systems

### When Adding New Analyses

1. **Prefer agent system** - Add new agents rather than standalone scripts
2. **Follow BaseAgent pattern** - Inherit and implement required methods
3. **Add configuration section** - Update config.yaml with new settings
4. **Document in agents/README.md** - Explain what the new agent does
5. **Write tests** - Add test cases in agents/test_agents.py

### Code Style Notes

- **Language**: Code comments and variable names are in Chinese (Traditional)
- **Logging**: All agents use structured logging via Python's logging module
- **Error Messages**: Preserve Chinese error messages for consistency
- **Data Validation**: Always validate inputs before processing

## Troubleshooting

### Common Issues

**Problem**: Chinese characters display as squares in charts
- **Solution**: Clear matplotlib font cache: `rm -rf ~/.matplotlib/fontlist-*.json`

**Problem**: Timezone conversion incorrect
- **Solution**: Verify using pytz.timezone() not fixed UTC offsets; pytz handles DST automatically

**Problem**: Agent execution fails silently
- **Solution**: Check `metadata["errors"]` in agent results; review logs for stack traces

**Problem**: Data appears empty after filtering
- **Solution**: Verify business rules match data (operating days, months, hours); check date range

**Problem**: MCP Square API calls fail
- **Solution**: Verify Square API access via Claude Code's MCP integration; check location ID

### Performance Optimization

- Enable parallel execution in config.yaml (`performance.parallel_execution: true`)
- Increase batch_size for large datasets
- Enable caching in data_agent config for repeated analyses
- Use date range filtering to reduce data processed

## Important Architectural Principles

1. **Separation of Concerns**: Each agent handles one domain (sales/customer/financial)
2. **Configuration Over Code**: Business rules and thresholds live in config.yaml
3. **Fail Gracefully**: Individual agent failures don't crash the entire system
4. **Timezone Correctness**: All timestamps use pytz for DST-aware conversion
5. **Data Integrity**: Deduplication and validation happen in DataAgent before analysis
6. **Extensibility**: New agents integrate without modifying existing ones
7. **Observability**: Comprehensive logging and metadata for debugging

## Related Documentation

For detailed information, refer to:
- [README.md](README.md) - Full project documentation
- [agents/ARCHITECTURE.md](agents/ARCHITECTURE.md) - Deep-dive architecture
- [agents/QUICKSTART.md](agents/QUICKSTART.md) - Quick start guide
- [analysis_output/cost_analysis/README.md](analysis_output/cost_analysis/README.md) - Cost analysis details

## MCP Configuration

Add this configuration to your `claude_desktop_config.json` or `mcp.json` to enable Square API integration:

```json
{
  "mcpServers": {
    "square": {
      "command": "npx",
      "args": [
        "-y",
        "square-mcp-server",
        "start"
      ],
      "env": {
        "ACCESS_TOKEN": "EAAAlxAXyAX2g8wHL4fpggE4yv5-4S3mO8rFH756zst3fLf_lPPPhuI1LR0CNc7a",
        "SANDBOX": "false",
        "DISALLOW_WRITES": "true"
      }
    }
  }
}
```
