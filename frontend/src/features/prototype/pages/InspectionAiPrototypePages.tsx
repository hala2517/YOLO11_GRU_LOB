import { useState } from 'react'
import { toast } from 'sonner'
import { Button } from '../components/PrototypeUi'
import { Activity, BarChart3, CalendarDays, CheckSquare, ChevronDown, ChevronRight, Database, FileCheck2, FolderCheck, FolderSearch, Play, ServerCog, ShieldCheck, SlidersHorizontal, TrendingUp } from 'lucide-react'
import { cn } from '@/shared/lib/utils'

export function DataInspectionPage() {
  const [selectedReviewId, setSelectedReviewId] = useState(1)
  const reviewVideos = [
    {
      id: 1,
      fileName: 'CCTV 1_2026-03-18_09-30-00',
      date: '2026-03-18 09:30:00',
      duration: '30초',
      images: '12장',
    },
    {
      id: 2,
      fileName: 'CCTV 1_2026-03-19_10-20-00',
      date: '2026-03-19 10:20:00',
      duration: '30초',
      images: '10장',
    },
    {
      id: 3,
      fileName: 'CCTV 1_2026-03-20_14-10-00',
      date: '2026-03-20 14:10:00',
      duration: '15초',
      images: '8장',
    },
  ]

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">데이터 검수</h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            라벨링 완료된 데이터를 검토하고 AI 학습용 데이터셋을 확정합니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <CalendarDays className="size-4" aria-hidden="true" />
            날짜별 라벨링 이미지 검토
          </span>
          <button
            type="button"
            onClick={() => toast.success('데이터셋 확정 더미')}
            className="inline-flex h-9 items-center gap-2 rounded-full bg-primary/20 px-4 text-sm font-semibold text-foreground transition-colors hover:bg-primary/30 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <ShieldCheck className="size-4" aria-hidden="true" />
            선택 후 데이터셋 확정
          </button>
        </div>
      </header>

      <section className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card p-4">
        <span className="text-sm font-medium text-muted-foreground">
          CCTV 선택
        </span>
        <div className="flex flex-wrap gap-2">
          {Array.from({ length: 8 }, (_, index) => `${index + 1}번`).map((label, index) => (
            <button
              key={label}
              type="button"
              className={cn(
                "flex h-10 min-w-13 items-center justify-center rounded-md border px-4 text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                index === 0
                  ? "border-primary bg-primary/20 text-foreground"
                  : "border-border bg-card text-foreground hover:bg-muted",
              )}
            >
              {label}
            </button>
          ))}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[324px_1fr]">
        <section className="rounded-lg border border-border bg-card p-5">
          <h2 className="text-xl font-bold text-foreground">라벨링 완료 영상</h2>
          <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
            선택한 CCTV에서 라벨링이 끝난 이미지 세트를 검수할 영상 파일을 선택합니다.
          </p>

          <div className="mt-5 inline-flex items-center rounded-full bg-primary/20 px-3 py-1.5 text-sm font-semibold text-foreground">
            CCTV 1
          </div>

          <div className="mt-5 space-y-2">
            {reviewVideos.map((video) => (
              <button
                key={video.id}
                type="button"
                onClick={() => setSelectedReviewId(video.id)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-md border p-4 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  selectedReviewId === video.id
                    ? "border-primary bg-primary/20"
                    : "border-border bg-card hover:bg-muted",
                )}
              >
                <FileCheck2 className="size-5 shrink-0 text-foreground" aria-hidden="true" />
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-bold text-foreground">
                    {video.fileName}
                  </span>
                  <span className="mt-2 block text-xs font-medium text-muted-foreground">
                    {video.date}
                  </span>
                  <span className="mt-2 flex gap-5 text-xs font-medium text-muted-foreground">
                    <span>{video.duration}</span>
                    <span>{video.images}</span>
                  </span>
                </span>
                <span className="shrink-0 rounded-full bg-status-success-bg px-3 py-1 text-xs font-semibold text-status-success-fg">
                  라벨링 완료
                </span>
              </button>
            ))}
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold text-foreground">
                이미지 검토 및 확정
              </h2>
              <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
                바운딩 박스가 포함된 이미지를 검토하고 불필요한 항목을 제외한 뒤 최종 데이터셋을 확정합니다.
              </p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-full bg-status-warning-bg px-3 py-1.5 text-sm font-semibold text-status-warning-fg">
              <CheckSquare className="size-4" aria-hidden="true" />
              검수 대기
            </span>
          </div>

          <div className="mt-5 flex min-h-[570px] items-center justify-center rounded-lg border border-dashed border-border bg-card p-8 text-center">
            <div className="max-w-md">
              <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-primary/20 text-primary">
                <FolderCheck className="size-7" aria-hidden="true" />
              </div>
              <h3 className="mt-7 text-xl font-bold text-foreground">
                검수할 영상을 선택해주세요.
              </h3>
              <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                좌측에서 라벨링 완료 영상을 선택하면 날짜별 이미지가 표시되며, 필요한 이미지를 골라 데이터셋을 확정할 수 있습니다.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}

export function AiTrainingPage() {
  const [dialogOpen, setDialogOpen] = useState(false)
  const trainingDatasets = [
    {
      id: 1,
      name: '작업자 감지_검수완료_2026-03-18',
      createdAt: '2026-03-18 16:24',
      images: '1,248장',
      cameras: 'CCTV 1 · CCTV 2',
    },
    {
      id: 2,
      name: '안전모 탐지_검수완료_2026-03-20',
      createdAt: '2026-03-20 11:10',
      images: '2,036장',
      cameras: 'CCTV 3 · CCTV 4 · CCTV 5',
    },
    {
      id: 3,
      name: 'AMR 접근감지_검수완료_2026-03-21',
      createdAt: '2026-03-21 09:42',
      images: '1,572장',
      cameras: 'CCTV 6 · CCTV 7',
    },
    {
      id: 4,
      name: '비인가자 접근_검수완료_2026-03-22',
      createdAt: '2026-03-22 14:05',
      images: '918장',
      cameras: 'CCTV 8',
    },
  ]

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">AI 모델 학습</h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            검수 완료된 데이터셋을 기반으로 AI 모델 학습을 수행합니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <Database className="size-4" aria-hidden="true" />
            검수 완료 데이터셋 선택
          </span>
          <button
            type="button"
            onClick={() => setDialogOpen(true)}
            className="inline-flex h-9 items-center gap-2 rounded-full bg-primary/20 px-4 text-sm font-semibold text-foreground transition-colors hover:bg-primary/30 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <Play className="size-4" aria-hidden="true" />
            수동 학습 시작 및 진행률 확인
          </button>
        </div>
      </header>

      <div className="grid gap-5 xl:grid-cols-[584px_1fr]">
        <div className="space-y-5">
          <section className="rounded-lg border border-border bg-card p-5">
            <h2 className="text-xl font-bold text-foreground">확정 데이터셋 선택</h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              데이터 검수 단계에서 확정된 데이터셋만 표시됩니다. 학습에 사용할 데이터셋을 하나 선택하세요.
            </p>

            <div className="mt-5 inline-flex items-center rounded-full bg-primary/20 px-3 py-1.5 text-sm font-semibold text-foreground">
              총 4개
            </div>

            <div className="mt-5 space-y-3">
              {trainingDatasets.map((dataset) => (
                <button
                  key={dataset.id}
                  type="button"
                  className="flex w-full items-center gap-4 rounded-md border border-border bg-card p-4 text-left transition-colors hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
                >
                  <Database className="size-6 shrink-0 text-foreground" aria-hidden="true" />
                  <span className="min-w-0 flex-1">
                    <span className="block truncate text-lg font-bold text-foreground">
                      {dataset.name}
                    </span>
                    <span className="mt-2 block text-xs font-medium text-muted-foreground">
                      생성일 {dataset.createdAt} · 이미지 {dataset.images}
                    </span>
                    <span className="mt-3 flex flex-wrap gap-4 text-sm font-semibold text-foreground">
                      <span className="rounded-full bg-status-success-bg px-3 py-1 text-status-success-fg">
                        확정됨
                      </span>
                      <span>{dataset.cameras}</span>
                    </span>
                  </span>
                  <ChevronRight className="size-5 text-foreground" aria-hidden="true" />
                </button>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-border bg-card p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold text-foreground">
                  선택 데이터셋 요약
                </h2>
                <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
                  선택한 데이터셋의 기본 정보를 확인한 뒤 모델을 선택하고 학습을 시작합니다.
                </p>
              </div>
              <span className="text-sm font-medium text-muted-foreground">
                선택 대기
              </span>
            </div>
            <div className="mt-5 flex min-h-[222px] items-center justify-center rounded-lg border border-dashed border-border bg-card p-8 text-center">
              <div className="max-w-md">
                <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-primary/20 text-primary">
                  <FolderSearch className="size-7" aria-hidden="true" />
                </div>
                <h3 className="mt-7 text-xl font-bold text-foreground">
                  데이터셋을 선택해주세요.
                </h3>
                <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                  좌측 목록에서 학습 대상 데이터셋을 선택하면 생성 날짜, 이미지 수, 상태 정보가 표시됩니다.
                </p>
              </div>
            </div>
          </section>
        </div>

        <div className="space-y-5">
          <section className="rounded-lg border border-border bg-card p-5">
            <h2 className="text-xl font-bold text-foreground">모델 선택 및 학습 제어</h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              데이터셋과 모델을 함께 선택한 후 사용자가 직접 학습을 시작합니다.
            </p>

            <div className="mt-5 inline-flex items-center gap-2 rounded-full bg-status-warning-bg px-3 py-1.5 text-sm font-semibold text-status-warning-fg">
              <ServerCog className="size-4" aria-hidden="true" />
              학습 준비 전
            </div>

            <label className="mt-6 block space-y-2 text-sm font-medium text-muted-foreground">
              <span>AI 모델 선택</span>
              <select className="h-11 w-full rounded-md border border-input bg-card px-4 text-sm font-medium text-muted-foreground outline-none focus:ring-2 focus:ring-ring">
                <option>데이터셋을 먼저 선택하세요</option>
              </select>
            </label>

            <p className="mt-3 text-xs font-medium text-muted-foreground">
              검수 완료 데이터셋과 모델 조합을 선택한 뒤 학습을 시작할 수 있습니다.
            </p>

            <div className="mt-6 flex items-center justify-between gap-4 rounded-lg border border-border bg-card p-4">
              <div>
                <h3 className="font-bold text-foreground">수동 실행 방식</h3>
                <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
                  데이터셋과 모델 선택이 완료되면 학습 시작 버튼이 활성화됩니다.
                </p>
              </div>
              <button
                type="button"
                disabled
                className="inline-flex h-11 shrink-0 items-center gap-2 rounded-md bg-primary px-5 text-sm font-semibold text-primary-foreground opacity-60"
              >
                <Play className="size-5" aria-hidden="true" />
                학습 시작
              </button>
            </div>
          </section>

          <section className="rounded-lg border border-border bg-card p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold text-foreground">학습 진행 상황</h2>
                <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
                  진행률, 예측 상태, 핵심 지표와 로그를 통해 학습 상태를 확인합니다.
                </p>
              </div>
              <span className="rounded-full bg-status-warning-bg px-3 py-1.5 text-sm font-semibold text-status-warning-fg">
                대기 중
              </span>
            </div>

            <div className="mt-5 flex min-h-[242px] items-center justify-center rounded-lg border border-dashed border-border bg-card p-8 text-center">
              <div className="max-w-md">
                <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-primary/20 text-primary">
                  <BarChart3 className="size-7" aria-hidden="true" />
                </div>
                <h3 className="mt-7 text-xl font-bold text-foreground">
                  학습이 아직 시작되지 않았습니다.
                </h3>
                <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                  데이터셋과 모델을 선택한 뒤 학습 시작 버튼을 누르면 진행률과 로그가 여기에 표시됩니다.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>

      {dialogOpen && <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"><div className="w-full max-w-md rounded-lg border border-border bg-card p-5"><h3 className="font-semibold text-foreground">학습 Job 생성</h3><div className="mt-4 space-y-3"><input className="w-full rounded-md border border-input bg-card px-3 py-2 text-foreground" placeholder="Job name" /><textarea className="w-full rounded-md border border-input bg-card px-3 py-2 text-foreground" placeholder='{"epochs": 50, "batch_size": 16}' /></div><div className="mt-5 flex justify-end gap-2"><Button variant="secondary" onClick={() => setDialogOpen(false)}>닫기</Button><Button onClick={() => { setDialogOpen(false); toast.success('학습 Job 생성 더미') }}>생성</Button></div></div></div>}
    </div>
  )
}

export function AiEvaluationPage() {
  const metrics = [
    { label: 'Accuracy', value: '95.6%', badge: '우수', hint: '전체 분류 정확도', tone: 'success' },
    { label: 'Precision', value: '94.3%', badge: '안정적', hint: '오탐 비율이 낮은 상태', tone: 'success' },
    { label: 'Recall', value: '92.8%', badge: '보통', hint: '일부 누락 탐지 구간 존재', tone: 'warning' },
    { label: 'F1 Score', value: '93.5%', badge: '균형 우수', hint: '정밀도와 재현율의 균형', tone: 'success' },
    { label: 'mAP', value: '94.2%', badge: '배포 후보', hint: '객체 탐지 종합 성능', tone: 'info' },
  ]
  const classes = ['헬멧 착용', '헬멧 미착용', '조끼 착용', '조끼 미착용']
  const matrix = [
    [186, 7, 4, 3],
    [9, 162, 2, 6],
    [5, 3, 175, 8],
    [4, 7, 6, 168],
  ]
  const prPoints = [
    { left: '8%', top: '16%' },
    { left: '22%', top: '18%' },
    { left: '36%', top: '21%' },
    { left: '50%', top: '26%' },
    { left: '64%', top: '34%' },
    { left: '78%', top: '45%' },
    { left: '92%', top: '57%' },
  ]

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header>
        <h1 className="text-3xl font-bold text-foreground">모델 평가 결과</h1>
        <p className="mt-3 text-sm font-medium text-muted-foreground">
          학습 완료된 AI 모델의 성능 지표와 평가 결과를 확인할 수 있습니다.
        </p>
      </header>

      <section className="rounded-lg border border-border bg-card p-4">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <label className="block space-y-2 text-sm font-medium text-muted-foreground">
            <span>모델 버전 선택</span>
            <div className="relative">
              <select className="h-10 w-60 appearance-none rounded-md border border-input bg-card px-4 pr-10 text-sm font-medium text-foreground outline-none focus:ring-2 focus:ring-ring">
                <option>작업자 안전장비 감지 · v2.4.1</option>
              </select>
              <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" aria-hidden="true" />
            </div>
          </label>
          <span className="mt-9 inline-flex items-center rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
            평가 결과 로드됨
          </span>
        </div>

        <div className="mt-4 grid gap-3 md:grid-cols-4">
          {[
            ['모델명', '작업자 안전장비 감지'],
            ['버전', 'v2.4.1'],
            ['학습 날짜', '2025-03-12'],
            ['데이터셋 규모 (이미지 수)', '124,320장'],
          ].map(([label, value]) => (
            <div key={label} className="rounded-md border border-border bg-card p-4">
              <p className="text-xs font-medium text-muted-foreground">{label}</p>
              <p className="mt-4 text-lg font-bold text-foreground">{value}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-lg border border-border bg-card p-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-foreground">핵심 성능 지표</h2>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              선택한 모델 버전의 주요 평가 지표를 한눈에 비교할 수 있습니다.
            </p>
          </div>
          <span className="inline-flex items-center rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
            기준 데이터셋: 검증 세트
          </span>
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-5">
          {metrics.map((metric) => (
            <div key={metric.label} className="rounded-md border border-border bg-card p-4">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-medium text-muted-foreground">{metric.label}</p>
                <span
                  className={cn(
                    "inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold",
                    metric.tone === 'warning' && "bg-status-warning-bg text-status-warning-fg",
                    metric.tone === 'success' && "bg-status-success-bg text-status-success-fg",
                    metric.tone === 'info' && "bg-status-info-bg text-status-info-fg",
                  )}
                >
                  {metric.tone === 'warning' ? <Activity className="size-3" /> : <TrendingUp className="size-3" />}
                  {metric.badge}
                </span>
              </div>
              <p className="mt-7 text-3xl font-bold text-foreground">{metric.value}</p>
              <p className="mt-4 text-xs font-medium text-muted-foreground">{metric.hint}</p>
            </div>
          ))}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-2">
        <section className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold text-foreground">Confusion Matrix</h2>
              <p className="mt-2 text-sm font-medium text-muted-foreground">
                실제 클래스와 예측 클래스 간 분포를 확인합니다.
              </p>
            </div>
            <span className="rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
              4개 클래스
            </span>
          </div>

          <div className="mt-5 rounded-md border border-border bg-card p-4">
            <div className="grid grid-cols-[96px_repeat(4,1fr)] gap-2 text-center text-xs font-medium text-muted-foreground">
              <span />
              {classes.map((klass) => <span key={klass}>{klass}</span>)}
              {matrix.map((row, rowIndex) => (
                <>
                  <span key={`row-${classes[rowIndex]}`} className="flex items-center justify-end pr-3">{classes[rowIndex]}</span>
                  {row.map((value, colIndex) => (
                    <span
                      key={`${rowIndex}-${colIndex}`}
                      className={cn(
                        "flex h-16 items-center justify-center rounded-md text-base font-bold text-foreground",
                        rowIndex === colIndex ? "bg-primary" : "bg-primary/20",
                      )}
                    >
                      {value}
                    </span>
                  ))}
                </>
              ))}
            </div>

            <div className="mt-6 flex flex-wrap items-center justify-center gap-6 text-sm font-medium text-muted-foreground">
              <span>낮음</span>
              <div className="h-2 w-44 rounded-full bg-primary" />
              <span>높음</span>
              <span className="rounded-full bg-muted px-3 py-1 text-foreground">대각선 집중도 높음</span>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-4">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold text-foreground">Precision-Recall Curve</h2>
              <p className="mt-2 text-sm font-medium text-muted-foreground">
                정밀도와 재현율의 관계를 시각적으로 확인합니다.
              </p>
            </div>
            <span className="rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
              AP 0.942
            </span>
          </div>

          <div className="mt-5 rounded-md border border-border bg-card p-6">
            <div className="relative h-[330px] border-l-4 border-b-4 border-border">
              <div className="absolute inset-x-6 bottom-6 top-12 bg-status-info-bg" />
              <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
                <polyline points="8,16 22,18 36,21 50,26 64,34 78,45 92,57" fill="none" stroke="var(--accent)" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              {prPoints.map((point) => (
                <span
                  key={`${point.left}-${point.top}`}
                  className="absolute size-5 rounded-full border-4 border-background bg-accent"
                  style={{ left: point.left, top: point.top }}
                />
              ))}
              <span className="absolute -left-11 top-1/2 -rotate-90 text-sm font-medium text-muted-foreground">Precision</span>
              <span className="absolute bottom-[-34px] right-0 text-sm font-medium text-muted-foreground">1.0 Recall</span>
            </div>
            <div className="mt-8 flex flex-wrap items-center justify-between gap-3 text-sm font-medium text-foreground">
              <span className="rounded-full bg-muted px-3 py-1">고재현율 구간에서도 정밀도 유지</span>
              <span className="inline-flex items-center gap-2 rounded-full bg-muted px-3 py-1">
                <SlidersHorizontal className="size-4" aria-hidden="true" />
                권장 임계값 0.63
              </span>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
