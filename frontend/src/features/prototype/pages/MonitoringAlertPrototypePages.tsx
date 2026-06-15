import { useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "sonner";
import {
  Activity,
  AlertTriangle,
  ArrowLeft,
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  FileText,
  Grid2X2,
  ListFilter,
  Maximize2,
  MapPin,
  Monitor,
  Pause,
  RefreshCw,
  ScanLine,
  Search,
  Signal,
  Table2,
  Video,
  VideoOff,
  Volume2,
} from "lucide-react";
import { cn } from "@/shared/lib/utils";

export function MonitoringDashboardPage() {
  const [autoRefresh, setAutoRefresh] = useState(false);
  const channelCards = [
    {
      id: 1,
      name: "CCTV 1",
      zone: "검사라인",
      status: "정상",
      online: true,
      fps: "30 FPS",
      resolution: "1920×1080",
    },
    {
      id: 2,
      name: "CCTV 2",
      zone: "포장라인",
      status: "정상",
      online: true,
      fps: "30 FPS",
      resolution: "1920×1080",
    },
    {
      id: 3,
      name: "CCTV 3",
      zone: "원료투입구역",
      status: "정상",
      online: true,
      fps: "30 FPS",
      resolution: "1920×1080",
    },
    {
      id: 4,
      name: "CCTV 4",
      zone: "출하 대기구역",
      status: "연결 끊김",
      online: false,
      fps: "스트림 점검 필요",
      resolution: "",
    },
    {
      id: 5,
      name: "CCTV 5",
      zone: "혼합공정라인",
      status: "정상",
      online: true,
      fps: "25 FPS",
      resolution: "1920×1080",
    },
    {
      id: 6,
      name: "CCTV 6",
      zone: "품질검사실 입구",
      status: "정상",
      online: true,
      fps: "30 FPS",
      resolution: "1280×720",
    },
    {
      id: 7,
      name: "CCTV 7",
      zone: "완제품 적치장",
      status: "정상",
      online: true,
      fps: "20 FPS",
      resolution: "1920×1080",
    },
    {
      id: 8,
      name: "CCTV 8",
      zone: "출입통제게이트",
      status: "정상",
      online: true,
      fps: "30 FPS",
      resolution: "1920×1080",
    },
  ];

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            작업현장 모니터링
          </h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            8대 CCTV를 통해 작업 현장을 실시간으로 관제할 수 있습니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-status-info-bg px-4 text-sm font-semibold text-status-info-fg">
            <Activity className="size-4" aria-hidden="true" />
            실시간 관제 활성화
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <Monitor className="size-4" aria-hidden="true" />총 8채널
          </span>
        </div>
      </header>

      <section className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card p-4">
        <button
          type="button"
          className="inline-flex h-10 items-center gap-2 rounded-md bg-primary/20 px-4 text-sm font-semibold text-foreground transition-colors hover:bg-primary/30 focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <Grid2X2 className="size-4" aria-hidden="true" />
          전체 채널 그리드
        </button>
        <button
          type="button"
          onClick={() => setAutoRefresh((value) => !value)}
          className="inline-flex h-10 items-center gap-2 rounded-md px-4 text-sm font-semibold text-foreground transition-colors hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <RefreshCw
            className={cn("size-4", autoRefresh && "animate-spin")}
            aria-hidden="true"
          />
          스트림 상태 새로고침
        </button>
        <p className="ml-auto text-sm font-medium text-muted-foreground">
          카메라 타일을 선택하면 해당 채널의 상세 모니터링 화면으로 이동합니다.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {channelCards.map((channel) => (
          <article
            key={channel.id}
            className="rounded-lg border border-border bg-card p-3"
          >
            <div className="flex items-center justify-between gap-3">
              <h2 className="text-lg font-bold text-foreground">
                {channel.name}
              </h2>
              <span
                className={cn(
                  "inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold",
                  channel.online
                    ? "bg-status-success-bg text-status-success-fg"
                    : "bg-status-error-bg text-status-error-fg",
                )}
              >
                <span className="size-2 rounded-full bg-current" />
                {channel.status}
              </span>
            </div>

            <div className="relative mt-3 aspect-video overflow-hidden rounded-md bg-muted">
              <div className="absolute inset-0 bg-gradient-to-br from-muted via-card to-background opacity-90" />
              <div className="absolute inset-0">
                <div className="absolute left-[-12%] top-[20%] h-1 w-[140%] rotate-32 bg-primary/20" />
                <div className="absolute left-[-18%] top-[58%] h-1 w-[140%] -rotate-32 bg-accent/10" />
              </div>
              <div className="absolute left-3 top-3 inline-flex items-center gap-2 rounded-full bg-status-error-bg px-3 py-1 text-xs font-bold text-status-error-fg">
                <span className="size-2 rounded-full bg-status-error-fg" />
                {channel.online ? "LIVE" : "OFFLINE"}
              </div>
              <span className="absolute right-3 top-3 text-xs font-semibold text-foreground">
                {channel.online
                  ? "2025-03-12 10:24:08"
                  : "마지막 수신 10:23:41"}
              </span>
              <div className="absolute bottom-5 left-4">
                <p className="text-base font-bold text-foreground">
                  {channel.name}
                </p>
                <p className="mt-1 text-sm font-semibold text-foreground">
                  {channel.zone}
                </p>
              </div>
              <Maximize2
                className="absolute bottom-5 right-4 size-5 text-foreground"
                aria-hidden="true"
              />
            </div>

            <div className="mt-3 flex items-center justify-between gap-3 text-sm font-medium text-muted-foreground">
              <div className="flex min-w-0 items-center gap-3">
                {channel.online ? (
                  <>
                    <span className="inline-flex items-center gap-1">
                      <Video className="size-4" aria-hidden="true" />
                      {channel.resolution}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <Signal className="size-4" aria-hidden="true" />
                      {channel.fps}
                    </span>
                  </>
                ) : (
                  <span className="inline-flex items-center gap-1">
                    <VideoOff className="size-4" aria-hidden="true" />
                    {channel.fps}
                  </span>
                )}
              </div>
              <a
                href={`/mornitoring/${channel.id}`}
                className="shrink-0 text-sm font-semibold text-primary hover:text-accent"
              >
                상세 보기
              </a>
            </div>
          </article>
        ))}
      </section>
    </div>
  );
}

export function MonitoringSiteDetailPage() {
  useParams();

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <a
          href="/mornitoring/dashboard"
          className="inline-flex h-10 items-center gap-2 rounded-md bg-card px-4 text-sm font-semibold text-foreground transition-colors hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <ArrowLeft className="size-4" aria-hidden="true" />
          목록으로 돌아가기
        </a>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-status-info-bg px-4 text-sm font-semibold text-status-info-fg">
            <Video className="size-4" aria-hidden="true" />
            CCTV 3
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <MapPin className="size-4" aria-hidden="true" />
            검사라인
          </span>
        </div>
      </div>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,726px)_398px]">
        <section className="rounded-lg border border-border bg-card p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h1 className="text-xl font-bold text-foreground">
                CCTV 3 실시간 영상
              </h1>
              <p className="mt-2 text-sm font-medium text-muted-foreground">
                검사라인 구역의 고해상도 실시간 영상을 모니터링합니다.
              </p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-full bg-status-success-bg px-3 py-1.5 text-sm font-semibold text-status-success-fg">
              <span className="size-2 rounded-full bg-current" />
              정상 연결
            </span>
          </div>

          <div className="relative mt-5 aspect-video overflow-hidden rounded-lg bg-muted">
            <div className="absolute inset-0 bg-gradient-to-br from-muted via-card to-background" />
            <div className="absolute left-[-12%] top-[18%] h-2 w-[140%] rotate-43 bg-accent/10" />
            <div className="absolute left-[-18%] top-[62%] h-2 w-[140%] -rotate-43 bg-primary/20" />
            <div className="absolute left-4 top-4 inline-flex items-center gap-2 rounded-full bg-status-error-bg px-3 py-1 text-xs font-bold text-status-error-fg">
              <span className="size-2 rounded-full bg-current" />
              LIVE
            </div>
            <span className="absolute left-20 top-4 rounded-full bg-status-info-bg px-3 py-1 text-xs font-bold text-status-info-fg">
              1920 x 1080
            </span>
            <span className="absolute right-5 top-5 text-sm font-semibold text-foreground">
              2026-03-18 14:32:08
            </span>
            <div className="absolute bottom-6 left-5">
              <h2 className="text-2xl font-bold text-foreground">CCTV 3</h2>
              <p className="mt-2 text-sm font-semibold text-foreground">
                검사라인 · 실시간 스트림 · 30 FPS
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
                <span className="rounded-full bg-status-info-bg px-3 py-1 text-xs font-semibold text-status-info-fg">
                  위치: 검사라인 A
                </span>
                <span className="rounded-full bg-status-info-bg px-3 py-1 text-xs font-semibold text-status-info-fg">
                  지연 0.8초
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 flex flex-wrap items-center gap-5">
            <button className="inline-flex h-10 items-center gap-2 rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground">
              <Pause className="size-4" aria-hidden="true" />
              일시정지
            </button>
            <div className="flex items-center gap-3 text-muted-foreground">
              <Volume2 className="size-5" aria-hidden="true" />
              <div className="h-2 w-24 rounded-full bg-accent" />
            </div>
          </div>

          <div className="mt-4 grid gap-3 md:grid-cols-3">
            {[
              ["해상도", "Full HD", "1920 x 1080"],
              ["스트림 상태", "안정", "패킷 손실 0.2%"],
              ["최근 연결 점검", "14:28", "4분 전 확인 완료"],
            ].map(([label, value, hint]) => (
              <div key={label} className="rounded-md bg-secondary p-4">
                <p className="text-xs font-medium text-muted-foreground">
                  {label}
                </p>
                <p className="mt-3 text-xl font-bold text-foreground">
                  {value}
                </p>
                <p className="mt-2 text-xs font-medium text-muted-foreground">
                  {hint}
                </p>
              </div>
            ))}
          </div>
        </section>

        <aside className="rounded-lg border border-border bg-card p-4">
          <h2 className="text-xl font-bold text-foreground">라인 정보</h2>
          <p className="mt-2 text-sm font-medium text-muted-foreground">
            선택한 CCTV와 연결된 생산 라인의 운영 현황을 확인합니다.
          </p>

          <dl className="mt-6 space-y-5 text-sm">
            {[
              ["라인명", "검사라인 A"],
              ["라인 ID", "LINE-INS-A03"],
              ["카메라 연결 상태", "정상"],
            ].map(([label, value]) => (
              <div
                key={label}
                className="flex items-center justify-between gap-4"
              >
                <dt className="font-medium text-muted-foreground">{label}</dt>
                <dd className="text-lg font-bold text-foreground">
                  {value === "정상" && (
                    <span className="mr-2 inline-block size-2 rounded-full bg-status-success-fg" />
                  )}
                  {value}
                </dd>
              </div>
            ))}
          </dl>

          <div className="my-6 h-px bg-border" />

          <section>
            <h3 className="text-lg font-bold text-foreground">
              가동 상태 정보
            </h3>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              현재 생산 라인의 운전 상태를 실시간으로 표시합니다.
            </p>
            <div className="mt-4 rounded-md bg-secondary p-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-muted-foreground">
                  현재 상태
                </span>
                <span className="rounded-full bg-status-success-bg px-3 py-1 text-sm font-semibold text-status-success-fg">
                  가동 중
                </span>
              </div>
              <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                설비, 카메라, 라인 연결 상태가 모두 안정적으로 유지되고
                있습니다.
              </p>
            </div>
          </section>

          <div className="my-6 h-px bg-border" />

          <section>
            <h3 className="text-lg font-bold text-foreground">
              가동 시간 정보
            </h3>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              오늘 기준 운영 시간과 연속 가동 시간을 제공합니다.
            </p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <div className="rounded-md bg-secondary p-4">
                <p className="text-xs font-medium text-muted-foreground">
                  오늘 가동 시간
                </p>
                <p className="mt-3 text-lg font-bold text-foreground">
                  6시간 32분
                </p>
              </div>
              <div className="rounded-md bg-secondary p-4">
                <p className="text-xs font-medium text-muted-foreground">
                  현재 연속 가동 시간
                </p>
                <p className="mt-3 text-lg font-bold text-foreground">
                  2시간 10분
                </p>
              </div>
            </div>
            <div className="mt-3 rounded-md bg-secondary p-4">
              <p className="text-xs font-medium text-muted-foreground">
                마지막 정지 시각
              </p>
              <p className="mt-3 text-lg font-bold text-foreground">
                2026-03-18 13:42
              </p>
            </div>
          </section>

          <section className="mt-5">
            <h3 className="text-lg font-bold text-foreground">
              간단 상태 요약
            </h3>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              운영자가 즉시 파악할 수 있는 한 줄 요약입니다.
            </p>
            <div className="mt-4 rounded-md bg-primary/20 p-4">
              <p className="font-bold text-foreground">
                현재 라인은 정상적으로 가동 중입니다.
              </p>
              <p className="mt-3 text-sm font-medium leading-6 text-foreground">
                검사라인 A에서 이상 상태 없이 작업이 진행되고 있으며 카메라 연결
                또한 정상입니다.
              </p>
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

export function UnauthorizedAlertPage() {
  const [selectedCctv, setSelectedCctv] = useState("CCTV 1");
  const detectionStats = [
    ["감지된 작업자 수", "2명", "실시간 프레임 기준"],
    ["비인가자 수", "1명", "지속 감지 기준 초과"],
    ["마지막 감지 시간", "10:45:18", "최근 경고 이벤트"],
  ];
  const events = [
    {
      title: "허용 색상 범위를 벗어난 안전모가 3초 이상 감지되었습니다.",
      time: "오늘 10:45:18",
      status: "경고",
      tone: "error",
    },
    {
      title: "인가 작업자 1명이 정상 색상으로 판별되었습니다.",
      time: "오늘 10:45:11",
      status: "정상",
      tone: "success",
    },
    {
      title: "기준 안전모 색상 프로파일이 갱신되었습니다.",
      time: "오늘 10:41:02",
      status: "설정",
      tone: "muted",
    },
  ];

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            비인가자 접근 알림 서비스
          </h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            작업자의 안전모 색상을 기준으로 인가 여부를 판별하고 비인가자 접근을
            감지합니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <ScanLine className="size-4" aria-hidden="true" />
            헬멧 색상 판별 모델 활성
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-status-error-bg px-4 text-sm font-semibold text-status-error-fg">
            <AlertTriangle className="size-4" aria-hidden="true" />
            비인가자 감지 주의
          </span>
        </div>
      </header>

      <section className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-xl font-bold text-foreground">CCTV 선택</h2>
        <p className="mt-2 text-sm font-medium text-muted-foreground">
          카메라를 변경하면 해당 구역의 실시간 감시 화면과 감지 상태가 함께
          갱신됩니다.
        </p>
        <div className="mt-5 flex flex-wrap gap-2">
          {Array.from({ length: 8 }, (_, index) => `CCTV ${index + 1}`).map(
            (label) => (
              <button
                key={label}
                type="button"
                onClick={() => setSelectedCctv(label)}
                className={cn(
                  "flex h-10 min-w-19 items-center justify-center rounded-md border px-4 text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  selectedCctv === label
                    ? "border-primary bg-primary/20 text-foreground"
                    : "border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                {label}
              </button>
            ),
          )}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,750px)_374px]">
        <div className="space-y-5">
          <section className="rounded-lg border border-border bg-card p-4">
            <div className="flex flex-wrap items-start justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold text-foreground">
                  실시간 감지 미리보기
                </h2>
                <p className="mt-2 text-sm font-medium text-muted-foreground">
                  안전모 색상 분류 결과, 신뢰도, 비인가자 판별 상태를 실시간으로
                  표시합니다.
                </p>
              </div>
              <span className="inline-flex items-center gap-2 rounded-full bg-status-error-bg px-3 py-1.5 text-sm font-semibold text-status-error-fg">
                <span className="size-2 rounded-full bg-current" />
                비인가자 감지
              </span>
            </div>

            <div className="mt-5 aspect-video rounded-lg border border-border bg-muted shadow-inner" />
          </section>

          <section className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-xl font-bold text-foreground">
              현재 감지 현황
            </h2>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              선택된 카메라의 작업자 감지 현황과 최근 판별 결과를 요약합니다.
            </p>
            <div className="mt-5 grid gap-3 md:grid-cols-3">
              {detectionStats.map(([label, value, hint]) => (
                <div key={label} className="rounded-md bg-secondary p-4">
                  <p className="text-sm font-medium text-muted-foreground">
                    {label}
                  </p>
                  <p className="mt-3 text-2xl font-bold text-foreground">
                    {value}
                  </p>
                  <p className="mt-2 text-xs font-medium text-muted-foreground">
                    {hint}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </div>

        <aside className="space-y-5">
          <section className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-xl font-bold text-foreground">감지 설정</h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              허용 색상 편차와 알람 발생 시간을 조정해 현장별 판정 기준을
              설정합니다.
            </p>

            <div className="mt-5">
              <div className="flex items-center justify-between">
                <label className="font-bold text-foreground">
                  색상 허용 오차 범위
                </label>
                <span className="rounded-md border border-border px-3 py-2 text-sm font-bold text-foreground">
                  38%
                </span>
              </div>
              <div className="mt-4 h-2 rounded-full bg-muted">
                <div className="h-full w-[38%] rounded-full bg-accent" />
              </div>
              <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                기존 안전모 색상에서 허용되는 색상 범위를 설정합니다. 값이
                높을수록 더 넓은 색상 편차를 허용합니다.
              </p>
            </div>

            <label className="mt-5 block space-y-2">
              <span className="font-bold text-foreground">알람 발생 시간</span>
              <select className="h-11 w-full rounded-md border border-input bg-card px-4 text-sm font-medium text-foreground outline-none focus:ring-2 focus:ring-ring">
                <option>3초 이상 감지 시 알람 발생</option>
              </select>
            </label>
            <p className="mt-3 text-sm font-medium leading-6 text-muted-foreground">
              비인가 안전모 색상이 설정된 시간 이상 지속적으로 감지될 때만 알람
              이벤트가 생성됩니다.
            </p>
          </section>

          <section className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-xl font-bold text-foreground">
              실시간 상태 패널
            </h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              현재 감지된 인원 수, 비인가자 수, 최근 갱신 시간을 빠르게
              확인합니다.
            </p>
            <div className="mt-5 space-y-3">
              {detectionStats.map(([label, value]) => (
                <div
                  key={label}
                  className="flex items-center justify-between rounded-md bg-secondary p-4"
                >
                  <span className="text-sm font-medium text-muted-foreground">
                    {label}
                  </span>
                  <strong className="text-lg text-foreground">{value}</strong>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-lg border border-border bg-card p-4">
            <h2 className="text-xl font-bold text-foreground">
              최근 감지 이벤트
            </h2>
            <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
              최근 안전모 색상 판별 이력을 시간 순으로 표시합니다.
            </p>
            <div className="mt-5 space-y-3">
              {events.map((event) => (
                <div key={event.title} className="rounded-md bg-secondary p-4">
                  <p className="text-sm font-bold leading-5 text-foreground">
                    {event.title}
                  </p>
                  <p className="mt-2 text-xs font-medium text-muted-foreground">
                    {event.time}
                  </p>
                  <span
                    className={cn(
                      "mt-4 inline-flex rounded-full px-3 py-1 text-xs font-semibold",
                      event.tone === "error" &&
                        "bg-status-error-bg text-status-error-fg",
                      event.tone === "success" &&
                        "bg-status-success-bg text-status-success-fg",
                      event.tone === "muted" &&
                        "bg-muted text-muted-foreground",
                    )}
                  >
                    {event.status}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}

export function AlertHistoryPage() {
  const eventRows = [
    {
      id: 24,
      occurredAt: "2025-03-20 10:45:18",
      type: "비인가자 접근",
      typeTone: "warning",
      location: "CCTV 1",
      target: "파란색 외 안전모 감지",
    },
    // {
    //   id: 23,
    //   occurredAt: "2025-03-20 10:41:06",
    //   type: "충돌 위험",
    //   typeTone: "error",
    //   location: "CCTV 4",
    //   target: "AMR-01 및 작업자 접근",
    // },
    {
      id: 22,
      occurredAt: "2025-03-20 10:35:52",
      type: "비인가자 접근",
      typeTone: "warning",
      location: "CCTV 3",
      target: "작업자 1명 - 흰색 안전모 감지",
    },
    // {
    //   id: 21,
    //   occurredAt: "2025-03-20 10:31:40",
    //   type: "충돌 위험",
    //   typeTone: "error",
    //   location: "CCTV 2",
    //   target: "AMR-02 접근 거리 임계값 초과",
    // },
    {
      id: 20,
      occurredAt: "2025-03-20 10:24:12",
      type: "비인가자 접근",
      typeTone: "warning",
      location: "CCTV 6",
      target: "노란색 기준 외 안전모 감지",
    },
    // {
    //   id: 19,
    //   occurredAt: "2025-03-20 10:19:45",
    //   type: "충돌 위험",
    //   typeTone: "error",
    //   location: "CCTV 5",
    //   target: "AMR-01 및 작업자 2명 접근",
    // },
  ];
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const selectedLog = eventRows.find((log) => log.id === selectedId);

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">
            이벤트 이력 관리
          </h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            현장에서 발생한 충돌 위험 및 비인가자 접근 알람 이력을 조회할 수
            있습니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-secondary px-4 text-sm font-semibold text-foreground">
            <RefreshCw className="size-4" aria-hidden="true" />
            운영 이력 조회 전용
          </span>
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-primary/20 px-4 text-sm font-semibold text-foreground">
            <Table2 className="size-4 text-primary" aria-hidden="true" />
            단일 테이블 요약 표시
          </span>
        </div>
      </header>

      <section className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-xl font-bold text-foreground">검색 조건</h2>
        <p className="mt-2 text-sm font-medium text-muted-foreground">
          기간과 이벤트 유형을 설정한 뒤 조회 버튼을 눌러 이력 목록을
          확인하세요.
        </p>
        <div className="mt-5 grid gap-3 lg:grid-cols-[1.25fr_1fr_auto]">
          <label className="space-y-2">
            <span className="block text-sm font-bold text-foreground">
              기간 설정
            </span>
            <span className="flex h-11 items-center justify-between rounded-md border border-input bg-secondary px-4 text-sm font-medium text-foreground">
              2025-03-01 00:00 ~ 2025-03-31 23:59
              <CalendarDays
                className="size-4 text-muted-foreground"
                aria-hidden="true"
              />
            </span>
          </label>
          <label className="space-y-2">
            <span className="block text-sm font-bold text-foreground">
              이벤트 유형
            </span>
            <select className="h-11 w-full rounded-md border border-input bg-secondary px-4 text-sm font-medium text-foreground outline-none focus:ring-2 focus:ring-ring">
              <option>전체</option>
              <option>비인가자 접근</option>
              <option>충돌 위험</option>
            </select>
          </label>
          <button
            type="button"
            onClick={() => toast.success("이벤트 이력을 조회했습니다.")}
            className="mt-auto inline-flex h-11 items-center justify-center gap-2 rounded-md bg-primary px-6 text-sm font-bold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <Search className="size-4" aria-hidden="true" />
            조회
          </button>
        </div>
      </section>

      <section className="rounded-lg border border-border bg-card p-4">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-foreground">
              이벤트 이력 목록
            </h2>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              행 클릭 없이 표에서 바로 발생 시점, 위치, 감지 대상을 확인할 수
              있습니다.
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex h-8 items-center gap-2 rounded-full border border-border px-3 text-xs font-semibold text-muted-foreground">
              <ListFilter className="size-3.5" aria-hidden="true" />
              전체 24건
            </span>
            <span className="inline-flex h-8 items-center gap-2 rounded-full border border-border px-3 text-xs font-semibold text-muted-foreground">
              <FileText className="size-3.5" aria-hidden="true" />1 / 4 페이지
            </span>
          </div>
        </div>

        <div className="mt-5 overflow-hidden rounded-md border border-border">
          <table className="w-full min-w-[820px] border-collapse text-left">
            <thead className="bg-muted text-xs font-bold text-muted-foreground">
              <tr>
                {[
                  "No",
                  "발생 일시",
                  "이벤트 유형",
                  "발생 위치",
                  "감지 대상",
                ].map((header) => (
                  <th key={header} className="px-4 py-4">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-border bg-card text-sm">
              {eventRows.map((row) => (
                <tr
                  key={row.id}
                  onClick={() => setSelectedId(row.id)}
                  className={cn(
                    "cursor-pointer transition-colors hover:bg-secondary",
                    row.typeTone === "error" &&
                      "border-l-2 border-l-status-error-fg",
                    row.typeTone === "warning" &&
                      "border-l-2 border-l-status-warning-fg",
                  )}
                >
                  <td className="px-4 py-4 font-bold text-foreground">
                    {row.id}
                  </td>
                  <td className="px-4 py-4 font-mono text-xs text-foreground">
                    {row.occurredAt}
                  </td>
                  <td className="px-4 py-4">
                    <span
                      className={cn(
                        "inline-flex rounded-full px-3 py-1 text-xs font-bold",
                        row.typeTone === "error" &&
                          "bg-status-error-bg text-status-error-fg",
                        row.typeTone === "warning" &&
                          "bg-status-warning-bg text-status-warning-fg",
                      )}
                    >
                      {row.type}
                    </span>
                  </td>
                  <td className="px-4 py-4 font-semibold text-foreground">
                    {row.location}
                  </td>
                  <td className="px-4 py-4 font-semibold text-foreground">
                    {row.target}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-5 flex items-center justify-center gap-2">
          <button
            className="inline-flex h-9 items-center gap-1 rounded-md border border-border px-3 text-sm font-semibold text-muted-foreground"
            type="button"
          >
            <ChevronLeft className="size-4" aria-hidden="true" />
            이전
          </button>
          {[1, 2, 3, 4].map((page) => (
            <button
              key={page}
              type="button"
              className={cn(
                "flex size-9 items-center justify-center rounded-md border text-sm font-semibold",
                page === 1
                  ? "border-primary bg-primary/20 text-foreground"
                  : "border-border text-muted-foreground hover:bg-secondary hover:text-foreground",
              )}
            >
              {page}
            </button>
          ))}
          <button
            className="inline-flex h-9 items-center gap-1 rounded-md border border-border px-3 text-sm font-semibold text-foreground"
            type="button"
          >
            다음
            <ChevronRight className="size-4" aria-hidden="true" />
          </button>
        </div>
      </section>

      {selectedLog && (
        <div className="fixed right-0 top-0 z-50 h-full w-full max-w-md border-l border-border bg-card p-6 shadow-xl">
          <h3 className="text-lg font-bold text-foreground">이벤트 상세</h3>
          <p className="mt-4 text-lg font-bold text-foreground">
            {selectedLog.type}
          </p>
          <p className="text-sm text-muted-foreground">
            {selectedLog.location} · {selectedLog.occurredAt}
          </p>
          <p className="mt-4 rounded-md bg-secondary p-4 text-sm font-semibold text-foreground">
            {selectedLog.target}
          </p>
          <pre className="mt-4 overflow-auto rounded bg-muted p-3 text-xs text-muted-foreground">
            {JSON.stringify(selectedLog, null, 2)}
          </pre>
          <div className="mt-4">
            <button
              type="button"
              onClick={() => setSelectedId(null)}
              className="h-10 rounded-md bg-primary px-4 text-sm font-bold text-primary-foreground"
            >
              닫기
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
