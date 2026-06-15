import { useState } from 'react'
import { toast } from 'sonner'
import {
  ArrowLeft,
  ArrowDownUp,
  BarChart3,
  CircleCheck,
  CircleX,
  Clock3,
  Database,
  Download,
  FileText,
  History,
  RefreshCw,
  Server,
  Settings2,
  X,
} from 'lucide-react'
import { cn } from '@/shared/lib/utils'

type LineRow = {
  id: string
  line: string
  productCode?: string
  productName?: string
  lob?: number
  eb?: number
  laborEfficiency?: string
  targetEndTime?: string
  expectedEndTime?: string
  note?: string
  tone?: 'success' | 'warning' | 'danger'
}

export function WorkerFlowPage() {
  const [selectedChartId, setSelectedChartId] = useState<string | null>(null)
  const [isCriteriaOpen, setIsCriteriaOpen] = useState(false)

  const criteria = {
    lobTarget: 92,
    lobWarning: 86,
    ebTarget: 88,
    ebWarning: 80,
    taktLimit: 4.2,
  }

  const lineRows: LineRow[] = [
    { id: 'SC30', line: 'SC30' },
    { id: 'SC31', line: 'SC31' },
    { id: 'SC32', line: 'SC32' },
    { id: 'SC33', line: 'SC33' },
    { id: 'SC34', line: 'SC34' },
    { id: 'SC35', line: 'SC35' },
    { id: 'SC36', line: 'SC36' },
    { id: 'SC37', line: 'SC37' },
    { id: 'SC38', line: 'SC38' },
    { id: 'SC39', line: 'SC39' },
    {
      id: 'SC40',
      line: 'SC40',
      productCode: '5023000-003',
      productName: '화장품크림-뿌잉',
      lob: 92,
      eb: 88,
      laborEfficiency: '-',
      targetEndTime: '-',
      expectedEndTime: '-',
      note: '-',
      tone: 'success',
    },
  ]

  const standardCharts = [
    {
      id: 'SPC-SC40-2026-01',
      lineId: 'SC40',
      name: '화장품크림-뿌잉 표준공정도',
      version: 'V1.0',
      status: '적용중',
      updatedAt: '2026-06-02',
      owner: '생산기술팀',
      lob: 92,
      eb: 88,
      dailyOutput: '7,695',
      hourlyOutput: '1,026',
      workerCount: 7,
      taktTime: '3.5',
      productCode: '5023000-003',
      productName: '화장품크림-뿌잉',
      processes: [
        { no: 1, name: '용기 공급', worker: '작업자 1', standardTime: 3.1, standardWorkers: 1, route: '충전 전처리', note: '공급대 고정' },
        { no: 2, name: '내용물 충전', worker: '작업자 2', standardTime: 4.2, standardWorkers: 1, route: '충전기', note: '점도 확인' },
        { no: 3, name: '캡 체결', worker: '작업자 3', standardTime: 3.6, standardWorkers: 1, route: '체결대', note: '토크 확인' },
        { no: 4, name: '로트 확인', worker: '작업자 4', standardTime: 2.8, standardWorkers: 1, route: '포장 투입', note: '인쇄 위치' },
        { no: 5, name: '라벨 부착', worker: '작업자 5', standardTime: 3.9, standardWorkers: 1, route: '자동 라벨러', note: '라벨 잔량' },
        { no: 6, name: '외관 검사', worker: '작업자 6', standardTime: 4.8, standardWorkers: 1, route: '검사대', note: '누액 검사' },
        { no: 7, name: '최종 포장', worker: '작업자 7', standardTime: 5.0, standardWorkers: 1, route: '출하 랙', note: '박스 적재' },
      ],
    },
  ]

  const selectedChart = standardCharts.find((chart) => chart.id === selectedChartId)
  const selectedLine = selectedChart
    ? lineRows.find((line) => line.id === selectedChart.lineId)
    : null
  const selectStandardChartByLine = (lineId: string) => {
    const chart =
      standardCharts.find((item) => item.lineId === lineId && item.status === '적용중') ??
      standardCharts.find((item) => item.lineId === lineId)

    if (!chart) {
      toast.error('해당 라인의 표준공정도를 찾을 수 없습니다.')
      return
    }

    setSelectedChartId(chart.id)
  }

  if (selectedChart && selectedLine) {
    const totalStandardTime = selectedChart.processes.reduce(
      (total, process) => total + process.standardTime,
      0,
    )

    return (
      <div className="mx-auto max-w-[1144px] space-y-5 text-foreground">
        <header className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <button
              type="button"
              onClick={() => setSelectedChartId(null)}
              className="mb-4 inline-flex h-9 items-center gap-2 rounded-md border border-border bg-card px-3 text-sm font-semibold text-foreground transition-colors hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <ArrowLeft className="size-4" aria-hidden="true" />
              라인 생산성 분석으로 돌아가기
            </button>
            <h1 className="text-[28px] font-bold leading-tight text-foreground">표준공정도</h1>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              {selectedLine.line} / {selectedChart.productCode} / {selectedChart.productName}
            </p>
          </div>
          <button
            type="button"
            onClick={() => toast.info('표준공정도 편집 기능은 다음 작업에서 연결됩니다.')}
            className="inline-flex h-10 items-center gap-2 rounded-md bg-primary px-4 text-sm font-bold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <Settings2 className="size-4" aria-hidden="true" />
            편집 준비
          </button>
        </header>

        <section className="rounded-lg border border-border bg-card p-6">
          <div className="grid gap-4 [@media(min-width:1500px)]:grid-cols-[minmax(420px,560px)_minmax(0,1fr)]">
            <ProcessStandardTable chart={selectedChart} totalStandardTime={totalStandardTime} />

            <div className="space-y-4">
              <ProcessSettingSummary
                lob={selectedChart.lob}
                eb={selectedChart.eb}
                totalStandardTime={totalStandardTime}
              />
              <ProcessMap />
            </div>
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_244px] xl:grid-cols-[464px_244px_minmax(0,1fr)]">
          <BasicInfoPanel chart={selectedChart} line={selectedLine.line} />
          <ReferenceImagePanel />
          <ProductionMetricsPanel chart={selectedChart} totalStandardTime={totalStandardTime} />
        </section>

        <p className="px-1 text-sm font-medium text-muted-foreground">
          표준공정도 사진 영역은 현재 더미 플레이스홀더로 표시됩니다.
        </p>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-[1144px] space-y-5 text-foreground">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-[28px] font-bold leading-tight text-foreground">라인 생산성 분석</h1>
          <p className="mt-2 text-sm font-medium text-muted-foreground">
            MES 생산 실적과 표준공정도 기준 LOB/EB를 비교합니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={() => setIsCriteriaOpen(true)}
            className="inline-flex h-10 items-center gap-2 rounded-md bg-primary px-4 text-sm font-bold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <Settings2 className="size-4" aria-hidden="true" />
            LOB/EB 기준 설정
          </button>
          <button
            type="button"
            onClick={() => toast.success('라인 생산성 데이터를 새로고침했습니다.')}
            className="inline-flex h-10 items-center gap-2 rounded-md border border-border bg-card px-4 text-sm font-semibold text-foreground transition-colors hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <RefreshCw className="size-4" aria-hidden="true" />
            새로고침
          </button>
        </div>
      </header>

      <section className="rounded-lg border border-border bg-card p-5">
        <div className="grid gap-4 md:grid-cols-3">
          <SummaryMetric label="LOB 목표 기준" value={`${criteria.lobTarget}%`} subText={`주의 ${criteria.lobWarning}% 미만`} />
          <SummaryMetric label="EB 목표 기준" value={`${criteria.ebTarget}%`} subText={`주의 ${criteria.ebWarning}% 미만`} />
          <SummaryMetric label="기준 충족 라인" value="1 / 11" subText="SC40 더미 데이터 기준" />
        </div>
      </section>

      <section className="rounded-lg border border-border bg-card p-5">
        <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-lg font-bold text-foreground">층별 생산성 데이터</h2>
            <p className="mt-1 text-sm font-medium text-muted-foreground">
              SC40을 선택하면 해당 라인의 표준공정도 페이지로 이동합니다.
            </p>
          </div>
          <span className="inline-flex h-8 items-center rounded-md border border-border px-3 text-xs font-bold text-muted-foreground">
            조회일 2026-06-02
          </span>
        </div>

        <div className="overflow-x-auto rounded-md border border-border">
          <table className="w-full min-w-[1060px] border-collapse text-left">
            <thead className="bg-muted text-xs font-bold text-muted-foreground">
              <tr>
                {['라인', '제품코드', '제품명', '생산성(LOB|EB)', '실동공수효율', '목표종료시간', '예상종료시간', '비고'].map((header) => (
                  <th key={header} className="border-b border-border px-4 py-3">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border bg-card text-sm">
              {lineRows.map((line) => (
                <tr key={line.id} className="transition-colors hover:bg-secondary">
                  <td className="px-4 py-4">
                    {line.id === 'SC40' ? (
                      <button
                        type="button"
                        onClick={() => selectStandardChartByLine(line.id)}
                        className="inline-flex h-8 min-w-20 items-center justify-center rounded-md border border-primary/30 bg-primary/15 px-3 text-sm font-bold text-foreground transition-colors hover:bg-primary/25 focus:outline-none focus:ring-2 focus:ring-ring"
                      >
                        {line.line}
                      </button>
                    ) : (
                      <span className="inline-flex h-8 min-w-20 items-center justify-center px-3 text-sm font-bold text-foreground">
                        {line.line}
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-4 font-mono text-xs font-bold text-foreground">{line.productCode ?? ''}</td>
                  <td className="px-4 py-4 font-bold text-foreground">{line.productName ?? ''}</td>
                  <td className="px-4 py-4">
                    {line.lob !== undefined && line.eb !== undefined && (
                      <span
                        className={cn(
                          'inline-flex rounded-md px-3 py-1 text-xs font-bold',
                          line.tone === 'success' && 'bg-status-success-bg text-status-success-fg',
                          line.tone === 'warning' && 'bg-status-warning-bg text-status-warning-fg',
                          line.tone === 'danger' && 'bg-status-error-bg text-status-error-fg',
                        )}
                      >
                        {line.lob}% | {line.eb}%
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-4 font-bold text-foreground">{line.laborEfficiency ?? ''}</td>
                  <td className="px-4 py-4 font-mono text-xs font-bold text-foreground">{line.targetEndTime ?? ''}</td>
                  <td className="px-4 py-4 font-mono text-xs font-bold text-foreground">{line.expectedEndTime ?? ''}</td>
                  <td className="px-4 py-4 font-semibold text-muted-foreground">{line.note ?? ''}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {isCriteriaOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
          <div className="w-full max-w-[620px] rounded-lg border border-border bg-card shadow-xl">
            <div className="flex items-start justify-between gap-4 border-b border-border p-5">
              <div>
                <h2 className="text-xl font-bold text-foreground">LOB/EB 기준 설정</h2>
                <p className="mt-2 text-sm font-medium text-muted-foreground">
                  라인 생산성 분석에서 사용할 목표 및 주의 기준을 설정합니다.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setIsCriteriaOpen(false)}
                className="flex size-9 items-center justify-center rounded-md border border-border text-foreground hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring"
                aria-label="기준 설정 닫기"
              >
                <X className="size-4" aria-hidden="true" />
              </button>
            </div>
            <div className="grid gap-4 p-5 sm:grid-cols-2">
              {[
                ['LOB 목표 기준', criteria.lobTarget, '%'],
                ['LOB 주의 기준', criteria.lobWarning, '%'],
                ['EB 목표 기준', criteria.ebTarget, '%'],
                ['EB 주의 기준', criteria.ebWarning, '%'],
                ['Tact Time 상한', criteria.taktLimit, '초'],
              ].map(([label, value, suffix]) => (
                <label key={label} className="block">
                  <span className="text-sm font-bold text-foreground">{label}</span>
                  <div className="mt-2 flex h-11 items-center rounded-md border border-input bg-background px-3 focus-within:ring-2 focus-within:ring-ring">
                    <input
                      defaultValue={value}
                      className="min-w-0 flex-1 bg-transparent text-sm font-bold text-foreground outline-none"
                    />
                    <span className="ml-2 text-sm font-bold text-muted-foreground">{suffix}</span>
                  </div>
                </label>
              ))}
              <label className="block sm:col-span-2">
                <span className="text-sm font-bold text-foreground">기준 설명</span>
                <textarea
                  defaultValue="LOB는 공정 균형률, EB는 라인 효율 기준으로 산정합니다. 기준 미달 라인은 표준공정도 재검토 대상으로 분류합니다."
                  className="mt-2 min-h-24 w-full rounded-md border border-input bg-background p-3 text-sm font-medium leading-6 text-foreground outline-none focus:ring-2 focus:ring-ring"
                />
              </label>
            </div>
            <div className="flex flex-wrap justify-end gap-3 border-t border-border p-5">
              <button
                type="button"
                onClick={() => setIsCriteriaOpen(false)}
                className="h-10 rounded-md border border-border bg-card px-4 text-sm font-bold text-foreground transition-colors hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring"
              >
                취소
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsCriteriaOpen(false)
                  toast.success('LOB/EB 기준을 저장했습니다.')
                }}
                className="inline-flex h-10 items-center gap-2 rounded-md bg-primary px-4 text-sm font-bold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <FileText className="size-4" aria-hidden="true" />
                저장
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function SummaryMetric({ label, value, subText }: { label: string; value: string; subText: string }) {
  return (
    <div className="rounded-md border border-border bg-secondary px-5 py-4">
      <p className="text-xs font-bold text-muted-foreground">{label}</p>
      <p className="mt-2 text-2xl font-bold text-foreground">{value}</p>
      <p className="mt-1 text-xs font-semibold text-muted-foreground">{subText}</p>
    </div>
  )
}

function ProcessStandardTable({
  chart,
  totalStandardTime,
}: {
  chart: {
    processes: {
      no: number
      name: string
      worker: string
      standardTime: number
      standardWorkers: number
      route: string
      note: string
    }[]
  }
  totalStandardTime: number
}) {
  const totalWorkers = chart.processes.reduce((total, process) => total + process.standardWorkers, 0)

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="grid grid-cols-[54px_1fr_64px_70px_110px] bg-muted text-center text-xs font-bold text-muted-foreground">
        {['No', '공정명', '인원', 'ST', '비고'].map((header) => (
          <div key={header} className="border-b border-r border-border px-2 py-3 last:border-r-0">
            {header}
          </div>
        ))}
      </div>
      <div className="text-xs font-semibold text-foreground">
        {chart.processes.map((process) => (
          <div key={process.no} className="grid grid-cols-[54px_1fr_64px_70px_110px]">
            <div className="border-b border-r border-border px-2 py-2 text-center">{process.no}</div>
            <div className="border-b border-r border-border px-2 py-2">{process.name}</div>
            <div className="border-b border-r border-border px-2 py-2 text-center">{process.standardWorkers}</div>
            <div className="border-b border-r border-border px-2 py-2 text-center">{process.standardTime.toFixed(1)}</div>
            <div className="border-b border-border px-2 py-2">{process.note}</div>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-[144px_168px_146px_1fr] bg-muted text-xs font-bold text-foreground">
        <div className="border-r border-border px-3 py-3">합계 Standard Time</div>
        <div className="border-r border-border px-3 py-3">{totalStandardTime.toFixed(1)}초</div>
        <div className="border-r border-border px-3 py-3">표준 인원</div>
        <div className="px-3 py-3">{totalWorkers}명</div>
      </div>
    </div>
  )
}

function ProcessSettingSummary({
  lob,
  eb,
  totalStandardTime,
}: {
  lob: number
  eb: number
  totalStandardTime: number
}) {
  return (
    <div className="grid h-[72px] grid-cols-3 rounded-lg border border-border bg-card">
      {[
        ['LOB', `${lob}%`, '균형률'],
        ['EB', `${eb}%`, '효율'],
        ['ST', totalStandardTime.toFixed(1), '초'],
      ].map(([label, value, unit], index) => (
        <div key={label} className={cn('px-5 py-3', index !== 2 && 'border-r border-border')}>
          <p className="text-xs font-bold text-muted-foreground">{label}</p>
          <div className="mt-2 flex items-end gap-1">
            <span className="text-xl font-bold text-foreground">{value}</span>
            <span className="pb-0.5 text-xs font-semibold text-muted-foreground">{unit}</span>
          </div>
        </div>
      ))}
    </div>
  )
}

function ProcessMap() {
  const workers = [
    [1, 50, 132],
    [2, 88, 118],
    [3, 126, 122],
    [4, 282, 128],
    [5, 298, 198],
    [6, 404, 130],
    [7, 508, 132],
  ] as const

  return (
    <div className="relative aspect-[560/328] w-full overflow-hidden rounded-lg border border-border bg-card">
      <div className="absolute flex items-center justify-center text-[clamp(12px,3.2vw,18px)] font-bold text-muted-foreground" style={rect(35, 18, 180, 30)}>충 전</div>
      <div className="absolute flex items-center justify-center text-[clamp(12px,3.2vw,18px)] font-bold text-muted-foreground" style={rect(232, 18, 270, 30)}>포 장</div>
      <div className="absolute bg-border" style={rect(196, 64, 1, 264)} />
      <div className="absolute rounded-md border border-border bg-status-success-bg" style={rect(18, 68, 170, 258)} />
      <div className="absolute rounded-md border border-border bg-secondary" style={rect(204, 68, 338, 258)} />

      <MapBlock rectValue={[36, 96, 116, 24]} className="bg-status-success-bg" label="용기 공급" />
      <MapBlock rectValue={[54, 154, 92, 30]} className="bg-primary/20" label="충전기" />
      <MapBlock rectValue={[64, 214, 92, 30]} className="bg-status-success-bg" label="캡 체결" />
      <div className="absolute rounded bg-status-success-fg/30" style={rect(220, 164, 296, 18)} />
      <span className="absolute text-[clamp(8px,2vw,11px)] font-semibold text-status-warning-fg" style={rect(226, 142, 90, 20)}>공정 흐름</span>
      <MapBlock rectValue={[220, 156, 32, 34]} className="bg-status-warning-bg" label="로트" />
      <MapBlock rectValue={[388, 120, 32, 52]} className="bg-primary/10" label="토트" />
      <MapBlock rectValue={[424, 150, 64, 40]} className="bg-status-info-bg" label="자동 라벨러" />
      <MapBlock rectValue={[512, 130, 26, 68]} className="bg-muted" label="외관 검사" />

      {workers.map(([number, left, top]) => (
        <div
          key={number}
          className="absolute flex -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full border-2 border-primary bg-card text-[clamp(8px,2vw,12px)] font-bold text-primary shadow-sm"
          style={{
            left: `${((left + 14) / 560) * 100}%`,
            top: `${((top + 14) / 328) * 100}%`,
            width: '5%',
            aspectRatio: '1 / 1',
          }}
        >
          {number}
        </div>
      ))}
      <p className="absolute text-center text-[clamp(8px,2vw,11px)] font-medium leading-[1.35] text-muted-foreground" style={rect(220, 286, 320, 22)}>
        RTSP/NVR 영상 위치와 작업자 공정 포인트를 함께 매핑할 수 있는 영역
      </p>
    </div>
  )
}

function MapBlock({
  rectValue,
  className,
  label,
}: {
  rectValue: [number, number, number, number]
  className: string
  label: string
}) {
  return (
    <div
      className={cn('absolute flex items-center justify-center rounded border border-border text-center text-[clamp(7px,1.9vw,10px)] font-semibold leading-[1.35] text-foreground', className)}
      style={rect(...rectValue)}
    >
      {label}
    </div>
  )
}

function rect(left: number, top: number, width: number, height: number) {
  return {
    left: `${(left / 560) * 100}%`,
    top: `${(top / 328) * 100}%`,
    width: `${(width / 560) * 100}%`,
    height: `${(height / 328) * 100}%`,
  }
}

function BasicInfoPanel({ chart, line }: { chart: { version: string; status: string; owner: string; updatedAt: string; productCode: string; productName: string }; line: string }) {
  return (
    <div className="h-[270px] rounded-lg border border-border bg-card p-5">
      <h2 className="text-lg font-bold text-foreground">기본 정보</h2>
      <div className="mt-4 border-t border-border pt-3">
        <div className="grid grid-cols-[92px_1fr_120px_1fr] text-xs font-semibold">
          <InfoLabel>라인</InfoLabel>
          <InfoValue>{line}</InfoValue>
          <InfoLabel>버전</InfoLabel>
          <InfoValue>{chart.version}</InfoValue>
          <InfoLabel>제품코드</InfoLabel>
          <InfoValue className="col-span-3">{chart.productCode}</InfoValue>
          <InfoLabel>제품명</InfoLabel>
          <InfoValue className="col-span-3">{chart.productName}</InfoValue>
        </div>
        <div className="mt-5 rounded-md border border-border">
          <div className="bg-muted px-4 py-2 text-xs font-bold text-muted-foreground">확인 항목</div>
          <div className="px-4 py-3 text-xs font-medium leading-5 text-muted-foreground">
            담당 {chart.owner} / 상태 {chart.status} / 최근 수정 {chart.updatedAt}
          </div>
        </div>
      </div>
    </div>
  )
}

function ReferenceImagePanel() {
  return (
    <div className="grid h-[270px] grid-cols-[48px_1fr] rounded-lg border border-border bg-card">
      <div className="flex items-center justify-center bg-muted text-sm font-bold text-muted-foreground [writing-mode:vertical-rl]">공정도 사진</div>
      <div className="flex items-center justify-center p-4">
        <div className="flex h-[202px] w-[162px] items-center justify-center rounded-md border border-dashed border-border bg-secondary text-center text-xs font-semibold leading-5 text-muted-foreground">
          이미지 영역
        </div>
      </div>
    </div>
  )
}

function ProductionMetricsPanel({
  chart,
  totalStandardTime,
}: {
  chart: { dailyOutput: string; hourlyOutput: string; workerCount: number; taktTime: string; lob: number; eb: number }
  totalStandardTime: number
}) {
  const metrics = [
    ['생산', '일일 생산량', chart.dailyOutput, 'ea/day'],
    ['생산', '시간당 생산량', chart.hourlyOutput, 'ea/hr'],
    ['공수', '작업자 수', `${chart.workerCount}`, '명'],
    ['공수', 'Tact Time', chart.taktTime, '초'],
    ['공수', 'Standard Time', totalStandardTime.toFixed(1), '초'],
    ['효율', 'LOB', `${chart.lob}`, '%'],
    ['효율', 'EB', `${chart.eb}`, '%'],
    ['비고', '개선 기준', chart.lob >= 90 ? '유지' : '재검토', ''],
  ]

  return (
    <div className="h-[270px] overflow-hidden rounded-lg border border-border bg-card lg:col-span-2 xl:col-span-1">
      <div className="grid grid-cols-[276px_1fr] border-b border-border text-center text-sm font-bold text-foreground">
        <div className="py-2">생산 지표</div>
        <div className="border-l border-border py-2">비고</div>
      </div>
      <div className="text-xs font-semibold text-foreground">
        {metrics.map(([group, label, value, note]) => (
          <div key={`${group}-${label}`} className="grid grid-cols-[52px_156px_68px_1fr] border-b border-border last:border-b-0">
            <div className="bg-muted px-2 py-1.5 text-center">{group}</div>
            <div className="border-l border-border px-2 py-1.5">{label}</div>
            <div className="border-l border-border px-2 py-1.5 text-right font-bold">{value}</div>
            <div className="border-l border-border px-2 py-1.5 text-muted-foreground">{note}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function InfoLabel({ children }: { children: string }) {
  return <div className="border-b border-border bg-muted px-3 py-3 text-muted-foreground">{children}</div>
}

function InfoValue({ children, className }: { children: string; className?: string }) {
  return <div className={cn('border-b border-border px-3 py-3 text-foreground', className)}>{children}</div>
}

export function MesIntegrationPage() {
  const syncLogs = [
    { id: 12, requestedAt: '2026-03-11 14:30:15', requester: 'Admin', status: '성공', tone: 'success', message: '정상 처리됨', active: true },
    { id: 11, requestedAt: '2026-03-11 09:12:40', requester: 'Admin', status: '실패', tone: 'error', message: 'DB 연결 오류' },
    { id: 10, requestedAt: '2026-03-10 18:05:23', requester: 'Admin', status: '성공', tone: 'success', message: '정상 처리됨' },
    { id: 9, requestedAt: '2026-03-10 11:48:02', requester: 'Manager', status: '성공', tone: 'success', message: '정상 처리됨' },
    { id: 8, requestedAt: '2026-03-09 16:33:14', requester: 'Admin', status: '실패', tone: 'error', message: '타임아웃' },
  ]

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">MES 연동</h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            외부 MES 시스템의 공정 데이터를 수동으로 동기화하고 연동 이력을 확인할 수 있습니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-secondary px-4 text-sm font-semibold text-foreground">
            <Database className="size-4" aria-hidden="true" />
            관리자 전용 수동 동기화
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-primary/20 px-4 text-sm font-semibold text-foreground">
            <History className="size-4 text-primary" aria-hidden="true" />
            최신 이력 우선 정렬
          </span>
        </div>
      </header>

      <section className="rounded-lg border border-border bg-card p-5">
        <div className="grid gap-6 lg:grid-cols-[1fr_280px]">
          <div>
            <h2 className="text-xl font-bold text-foreground">MES 동기화 제어</h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              버튼을 클릭하면 외부 MES 데이터베이스에 연결하여 저장 프로시저를 실행하고 최신 공정 데이터를 불러옵니다.
            </p>

            <div className="mt-7">
              <h3 className="text-2xl font-bold text-foreground">MES 데이터 수동 동기화</h3>
              <p className="mt-4 max-w-3xl text-sm font-medium leading-7 text-muted-foreground">
                외부 MES 시스템의 최신 생산 실적과 공정 정보를 즉시 조회하여 시스템에 반영합니다. 동기화 요청 시 새로운 로그가 생성되며, 처리 결과는 아래 이력 테이블에서 확인할 수 있습니다.
              </p>
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-3">
              <span className="inline-flex h-9 items-center gap-2 rounded-md border border-status-success-fg/25 bg-status-success-bg px-4 text-sm font-semibold text-status-success-fg">
                <Clock3 className="size-4" aria-hidden="true" />
                최근 동기화: 2026-03-11 14:30:15
              </span>
            </div>

            <div className="mt-3 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => toast.success('MES 데이터를 불러왔습니다.')}
                className="inline-flex h-11 items-center gap-2 rounded-md bg-primary px-5 text-sm font-bold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <Download className="size-4" aria-hidden="true" />
                MES 데이터 불러오기
              </button>
              <button
                type="button"
                onClick={() => toast.info('동기화 이력을 새로고침했습니다.')}
                className="inline-flex h-11 items-center gap-2 rounded-md border border-border bg-card px-5 text-sm font-bold text-foreground transition-colors hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <RefreshCw className="size-4" aria-hidden="true" />
                이력 새로고침
              </button>
            </div>
          </div>

          <aside className="space-y-3">
            <div className="flex justify-end gap-2">
              <span className="inline-flex h-8 items-center gap-2 rounded-full bg-status-success-bg px-3 text-xs font-bold text-status-success-fg">
                <CircleCheck className="size-3.5" aria-hidden="true" />
                최근 동기화 성공
              </span>
              <span className="inline-flex h-8 items-center gap-2 rounded-full border border-border px-3 text-xs font-bold text-muted-foreground">
                <Server className="size-3.5" aria-hidden="true" />
                읽기 전용 연동
              </span>
            </div>
            <div className="rounded-lg border border-border bg-secondary p-4">
              <p className="text-sm font-semibold text-muted-foreground">최근 요청자</p>
              <p className="mt-5 text-2xl font-bold text-foreground">Admin</p>
              <p className="mt-4 text-xs font-medium text-muted-foreground">최근 성공 요청 기준</p>
            </div>
            <div className="rounded-lg border border-border bg-secondary p-4">
              <p className="text-sm font-semibold text-muted-foreground">최근 응답 메시지</p>
              <p className="mt-5 text-2xl font-bold text-foreground">정상 처리됨</p>
              <p className="mt-4 text-xs font-medium text-muted-foreground">동기화 로그 테이블과 동일하게 반영</p>
            </div>
          </aside>
        </div>
      </section>

      <section className="rounded-lg border border-border bg-card p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-foreground">동기화 이력</h2>
            <p className="mt-3 text-sm font-medium text-muted-foreground">
              동기화 요청 결과는 요청 시각, 요청자, 처리 결과, 응답 메시지 기준으로 기록됩니다. 기본 정렬은 최신순입니다.
            </p>
          </div>
          <span className="inline-flex h-9 items-center gap-2 rounded-full border border-border px-4 text-sm font-semibold text-muted-foreground">
            <BarChart3 className="size-4" aria-hidden="true" />
            마지막 반영 14:30:15
          </span>
        </div>

        <div className="mt-5 flex flex-wrap gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full border border-border px-4 text-sm font-semibold text-muted-foreground">
            <Server className="size-4" aria-hidden="true" />
            총 12건
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-md border border-border px-4 text-sm font-semibold text-muted-foreground">
            <ArrowDownUp className="size-4" aria-hidden="true" />
            최신 요청 순
          </span>
        </div>

        <div className="mt-5 overflow-hidden rounded-md border border-border">
          <table className="w-full min-w-[820px] border-collapse text-left">
            <thead className="bg-muted text-xs font-bold text-muted-foreground">
              <tr>
                {['No', '요청 일시', '요청자', '연동 결과', '응답 메시지'].map((header) => (
                  <th key={header} className="px-4 py-4">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border bg-card text-sm">
              {syncLogs.map((log) => (
                <tr
                  key={log.id}
                  className={cn(
                    'transition-colors hover:bg-secondary',
                    log.active && 'bg-primary/10',
                  )}
                >
                  <td className="px-4 py-4 font-bold text-foreground">{log.id}</td>
                  <td className="px-4 py-4 font-mono text-xs text-foreground">{log.requestedAt}</td>
                  <td className="px-4 py-4 font-bold text-foreground">{log.requester}</td>
                  <td className="px-4 py-4">
                    <span
                      className={cn(
                        'inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold',
                        log.tone === 'success' && 'bg-status-success-bg text-status-success-fg',
                        log.tone === 'error' && 'bg-status-error-bg text-status-error-fg',
                      )}
                    >
                      {log.tone === 'success' ? <CircleCheck className="size-3.5" aria-hidden="true" /> : <CircleX className="size-3.5" aria-hidden="true" />}
                      {log.status}
                    </span>
                  </td>
                  <td className="px-4 py-4 font-bold text-foreground">{log.message}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-5 flex flex-wrap items-center justify-between gap-4">
          <p className="text-sm font-semibold text-muted-foreground">1-5 / 12건 표시</p>
          <div className="flex items-center gap-2">
            <button type="button" className="h-10 rounded-md border border-border px-4 text-sm font-semibold text-muted-foreground">
              이전
            </button>
            {[1, 2, 3].map((page) => (
              <button
                key={page}
                type="button"
                className={cn(
                  'flex size-10 items-center justify-center rounded-md border text-sm font-semibold',
                  page === 1
                    ? 'border-primary bg-primary/20 text-foreground'
                    : 'border-border text-muted-foreground hover:bg-secondary hover:text-foreground',
                )}
              >
                {page}
              </button>
            ))}
            <button type="button" className="h-10 rounded-md border border-border px-4 text-sm font-semibold text-foreground">
              다음
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}
