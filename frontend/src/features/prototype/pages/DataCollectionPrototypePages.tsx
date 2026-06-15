import { useState } from "react";
import { toast } from "sonner";
import { cameras, nvrs } from "@/shared/mock/prototypeData";
import {
  Button,
} from "../components/PrototypeUi";
import {
  Camera,
  CalendarDays,
  CheckCircle2,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Database,
  FileVideo,
  ImageIcon,
  Pause,
  Play,
  Plus,
  RefreshCw,
  SkipBack,
  SkipForward,
  Volume2,
  Wand2,
  Zap,
} from "lucide-react";
import { cn } from "@/shared/lib/utils";

export function DataCollectionEnvPage() {
  const [selectedNvrId, setSelectedNvrId] = useState(nvrs[0].id);
  const [dialogOpen, setDialogOpen] = useState(false);
  const selectedNvr = nvrs.find((nvr) => nvr.id === selectedNvrId) ?? nvrs[0];
  const cameraRows = [
    { id: "CCTV-01", name: "CCTV 1", line: "검사라인", status: "연결됨" },
    { id: "CCTV-02", name: "CCTV 2", line: "포장라인", status: "연결됨" },
    { id: "CCTV-03", name: "CCTV 3", line: "조립라인", status: "연결됨" },
    { id: "CCTV-04", name: "CCTV 4", line: "검수라인", status: "연결됨" },
    { id: "CCTV-05", name: "CCTV 5", line: "출하라인", status: "연결됨" },
  ];

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header>
        <h1 className="text-3xl font-bold text-foreground">데이터 수집 환경</h1>
        <p className="mt-3 text-sm font-medium text-muted-foreground">
          NVR 및 CCTV 장비를 등록하고 데이터 수집 환경을 설정할 수 있습니다.
        </p>
      </header>

      <section className="rounded-lg border border-border bg-card p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-foreground">NVR 등록</h2>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              시스템에서 인식할 NVR 장비를 등록합니다. 최소 정보만 입력해 초기 수집 환경을 빠르게 구성할 수 있습니다.
            </p>
          </div>
          <div className="inline-flex items-center gap-2 rounded-full border border-status-success-bg bg-status-success-bg px-4 py-2 text-sm font-medium text-status-success-fg">
            <CheckCircle2 className="size-4" aria-hidden="true" />
            현재 3개 NVR 등록됨
          </div>
        </div>

        <div className="mt-6 grid gap-4 lg:grid-cols-[1fr_1fr_1fr_1fr]">
          <label className="space-y-2 text-xs font-medium text-muted-foreground">
            <span>NVR 이름</span>
            <input
              className="h-10 w-full rounded-md border border-input bg-card px-4 text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
              defaultValue="예: 생산동 NVR-01"
            />
          </label>
          <label className="space-y-2 text-xs font-medium text-muted-foreground">
            <span>IP 주소</span>
            <input
              className="h-10 w-full rounded-md border border-input bg-card px-4 text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
              defaultValue="192.168.0.120"
            />
          </label>
          <label className="space-y-2 text-xs font-medium text-muted-foreground">
            <span>포트 번호</span>
            <input
              className="h-10 w-full rounded-md border border-input bg-card px-4 text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
              defaultValue="554"
            />
          </label>
          <label className="space-y-2 text-xs font-medium text-muted-foreground">
            <span>등록</span>
            <button
              type="button"
              onClick={() => toast.info("NVR 등록은 프로토타입 더미 처리입니다.")}
              className="flex h-10 w-full items-center justify-center gap-2 rounded-md bg-primary text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <Plus className="size-5" aria-hidden="true" />
              NVR 등록
            </button>
          </label>
        </div>

        <label className="mt-4 block max-w-[543px] space-y-2 text-xs font-medium text-muted-foreground">
          <span>간단한 설명</span>
          <textarea
            className="h-[88px] w-full resize-none rounded-md border border-input bg-card px-4 py-3 text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground focus:ring-2 focus:ring-ring"
            defaultValue="생산동 서측 라인 전용 녹화 장비"
          />
        </label>
      </section>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,674px)_1fr]">
        <div className="space-y-5">
          <section className="rounded-lg border border-border bg-card p-5">
            <h2 className="text-xl font-bold text-foreground">NVR 선택</h2>
            <p className="mt-2 text-sm font-medium text-muted-foreground">
              선택한 NVR에 연결된 CCTV 목록을 확인하고 신규 장비를 연결할 수 있습니다.
            </p>
            <label className="mt-6 block space-y-2 text-xs font-medium text-muted-foreground">
              <span>NVR 선택</span>
              <div className="relative">
                <select
                  value={selectedNvrId}
                  onChange={(event) => setSelectedNvrId(Number(event.target.value))}
                  className="h-10 w-full appearance-none rounded-md border border-input bg-card px-4 pr-10 text-sm font-medium text-foreground outline-none focus:ring-2 focus:ring-ring"
                >
                  {nvrs.map((nvr) => (
                    <option key={nvr.id} value={nvr.id}>
                      {nvr.id === 1 ? "생산동 NVR-01" : nvr.name}
                    </option>
                  ))}
                </select>
                <ChevronDown
                  className="pointer-events-none absolute right-4 top-1/2 size-4 -translate-y-1/2 text-muted-foreground"
                  aria-hidden="true"
                />
              </div>
            </label>
          </section>

          <section className="rounded-lg border border-border bg-card p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-bold text-foreground">
                  연결된 CCTV 목록
                </h2>
                <p className="mt-2 text-sm font-medium text-muted-foreground">
                  선택한 NVR에 연결된 카메라와 작업 라인 정보를 조회합니다.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="inline-flex h-8 items-center gap-2 rounded-full border border-border px-3 text-xs font-medium text-muted-foreground">
                  <Database className="size-4" aria-hidden="true" />총 8대
                </span>
                <button
                  type="button"
                  onClick={() => setDialogOpen(true)}
                  className="flex h-10 items-center gap-2 rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
                >
                  <Camera className="size-5" aria-hidden="true" />
                  신규 CCTV 추가
                </button>
              </div>
            </div>

            <div className="mt-5 overflow-hidden rounded-lg border border-border">
              <table className="w-full text-sm">
                <thead className="bg-muted">
                  <tr className="text-left text-xs font-semibold text-muted-foreground">
                    <th className="px-4 py-4">CCTV ID</th>
                    <th className="px-4 py-4">CCTV 이름</th>
                    <th className="px-4 py-4">연결 상태</th>
                    <th className="px-4 py-4">작업 라인</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {cameraRows.map((camera) => (
                    <tr key={camera.id} className="transition-colors hover:bg-muted/40">
                      <td className="px-4 py-4 font-medium text-foreground">
                        <span className="mr-2 inline-block size-2 rounded-full bg-accent" />
                        {camera.id}
                      </td>
                      <td className="px-4 py-4 font-medium text-foreground">
                        {camera.name}
                      </td>
                      <td className="px-4 py-4">
                        <span className="inline-flex items-center gap-1.5 rounded-full bg-status-success-bg px-2.5 py-1 text-xs font-semibold text-status-success-fg">
                          <CheckCircle2 className="size-3.5" aria-hidden="true" />
                          {camera.status}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <span className="inline-flex rounded-full bg-primary/20 px-3 py-1 text-xs font-medium text-foreground">
                          {camera.line}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mt-5 flex items-center justify-between text-sm font-medium text-muted-foreground">
              <span>1-5 / 8건 표시</span>
              <div className="flex items-center gap-3">
                <button className="flex h-9 items-center gap-2 rounded-md border border-border px-4 text-foreground transition-colors hover:bg-muted">
                  <ChevronLeft className="size-4" aria-hidden="true" /> 이전
                </button>
                <button className="flex size-9 items-center justify-center rounded-md border border-primary bg-primary/20 text-primary">
                  1
                </button>
                <button className="flex size-9 items-center justify-center rounded-md border border-border text-foreground transition-colors hover:bg-muted">
                  2
                </button>
                <button className="flex h-9 items-center gap-2 rounded-md border border-border px-4 text-foreground transition-colors hover:bg-muted">
                  다음 <ChevronRight className="size-4" aria-hidden="true" />
                </button>
              </div>
            </div>
          </section>
        </div>

        <section className="rounded-lg border border-border bg-card p-5">
          <h2 className="text-xl font-bold text-foreground">선택된 NVR 요약</h2>
          <p className="mt-2 text-sm font-medium text-muted-foreground">
            현재 선택한 장비의 기본 연결 정보와 CCTV 연결 현황입니다.
          </p>

          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs font-medium text-muted-foreground">NVR 이름</p>
              <p className="mt-4 text-xl font-bold text-foreground">
                {selectedNvr.id === 1 ? "생산동 NVR-01" : selectedNvr.name}
              </p>
              <p className="mt-2 text-xs font-medium text-muted-foreground">
                생산동 서측 구역 녹화 장비
              </p>
            </div>
            <div className="rounded-lg border border-border bg-card p-4">
              <p className="text-xs font-medium text-muted-foreground">IP 주소</p>
              <p className="mt-4 text-xl font-bold text-foreground">
                {selectedNvr.id === 1 ? "192.168.0.120" : selectedNvr.ip}
              </p>
              <p className="mt-2 text-xs font-medium text-muted-foreground">
                RTSP 포트 {selectedNvr.port} 사용
              </p>
            </div>
          </div>

          <div className="mt-4 rounded-lg border border-border bg-card p-4">
            <p className="text-xs font-medium text-muted-foreground">연결된 CCTV 수</p>
            <p className="mt-4 text-xl font-bold text-foreground">8대</p>
            <p className="mt-2 text-xs font-medium text-muted-foreground">
              연결됨 7대 / 미연결 1대
            </p>
          </div>

          <div className="mt-5">
            <h3 className="font-bold text-foreground">운영 메모</h3>
            <p className="mt-3 text-sm font-medium leading-6 text-muted-foreground">
              선택한 NVR의 CCTV는 라인별 데이터 수집 그룹과 연결됩니다. 신규 CCTV를 등록한 뒤 작업 라인을 지정하면 수집 페이지에서 즉시 구분 가능합니다.
            </p>
          </div>

          <div className="mt-4 inline-flex w-full items-center gap-2 rounded-full border border-border px-4 py-2 text-sm font-medium text-muted-foreground">
            <Zap className="size-4" aria-hidden="true" />
            최근 상태 점검: 정상
          </div>
        </section>
      </div>

      {dialogOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-md rounded-lg border border-border bg-card p-5">
            <h3 className="font-semibold">CCTV 추가/수정</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              프로토타입 더미 dialog입니다.
            </p>
            <div className="mt-4 space-y-3">
              <input
                className="w-full rounded-md border border-input bg-background px-3 py-2"
                placeholder="Camera name"
              />
              <input
                className="w-full rounded-md border border-input bg-background px-3 py-2"
                placeholder="RTSP URL"
              />
            </div>
            <div className="mt-5 flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setDialogOpen(false)}>
                닫기
              </Button>
              <Button
                onClick={() => {
                  setDialogOpen(false);
                  toast.success("CCTV 저장 더미 완료");
                }}
              >
                저장
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export function DataCollectionJobsPage() {
  const [cameraName, setCameraName] = useState(cameras[0].name);
  const [selectedVideoId, setSelectedVideoId] = useState(1);
  const videoRows = [
    {
      id: 1,
      fileName: "CAM01_2025-03-12_14-30-00.mp4",
      start: "14:30:00",
      status: "정상 저장",
      duration: "30초",
    },
    {
      id: 2,
      fileName: "CAM01_2025-03-12_14-29-30.mp4",
      start: "14:29:30",
      status: "정상 저장",
      duration: "30초",
    },
    {
      id: 3,
      fileName: "CAM01_2025-03-12_14-29-15.mp4",
      start: "14:29:15",
      status: "이벤트 구간",
      duration: "15초",
    },
    {
      id: 4,
      fileName: "CAM01_2025-03-12_14-28-45.mp4",
      start: "14:28:45",
      status: "정상 저장",
      duration: "30초",
    },
    {
      id: 5,
      fileName: "CAM01_2025-03-12_14-28-15.mp4",
      start: "14:28:15",
      status: "정상 저장",
      duration: "30초",
    },
    {
      id: 6,
      fileName: "CAM01_2025-03-12_14-27-45.mp4",
      start: "14:27:45",
      status: "정상 저장",
      duration: "30초",
    },
    {
      id: 7,
      fileName: "CAM01_2025-03-12_14-27-30.mp4",
      start: "14:27:30",
      status: "이벤트 구간",
      duration: "15초",
    },
  ];
  const selectedVideo =
    videoRows.find((video) => video.id === selectedVideoId) ?? videoRows[0];

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header>
        <h1 className="text-3xl font-bold text-foreground">데이터 수집</h1>
        <p className="mt-3 text-sm font-medium text-muted-foreground">
          저장된 CCTV 영상 파일을 조회하고 재생할 수 있습니다.
        </p>
      </header>

      <section className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card p-4">
        <span className="text-sm font-medium text-muted-foreground">
          CCTV 선택
        </span>
        <div className="flex flex-wrap gap-2">
          {Array.from({ length: 8 }, (_, index) => `${index + 1}번`).map(
            (label) => (
              <button
                key={label}
                type="button"
                onClick={() => setCameraName(label)}
                className={cn(
                  "flex h-10 min-w-13 items-center justify-center rounded-md border px-4 text-sm font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  cameraName === label || (cameraName === cameras[0].name && label === "1번")
                    ? "border-primary bg-primary text-primary-foreground"
                    : "border-border bg-card text-foreground hover:bg-muted",
                )}
              >
                {label}
              </button>
            ),
          )}
        </div>

        <div className="ml-auto flex flex-wrap items-center gap-3">
          <span className="text-sm font-medium text-muted-foreground">
            조회 일시
          </span>
          <div className="flex h-10 min-w-[230px] items-center gap-3 rounded-md border border-input bg-card px-4 text-sm font-medium text-foreground">
            <CalendarDays className="size-5 text-foreground" aria-hidden="true" />
            2025-03-12 14:30
          </div>
          <button
            type="button"
            onClick={() => toast.info("영상 목록 새로고침")}
            className="flex h-10 items-center gap-2 rounded-md px-3 text-sm font-semibold text-foreground transition-colors hover:bg-muted focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <RefreshCw className="size-5" aria-hidden="true" />
            새로고침
          </button>
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[minmax(0,735px)_390px]">
        <section className="rounded-lg border border-border bg-card p-5">
          <div className="flex items-center gap-2 text-sm font-bold text-accent">
            <Camera className="size-4" aria-hidden="true" />
            선택된 녹화 파일
          </div>
          <h2 className="mt-3 text-xl font-bold text-foreground">
            {selectedVideo.fileName}
          </h2>
          <div className="mt-4 flex flex-wrap gap-7 text-sm font-medium text-foreground">
            <span>CCTV 1번</span>
            <span>녹화 시작 {selectedVideo.start}</span>
            <span>재생 길이 {selectedVideo.duration}</span>
          </div>

          <div className="mt-6 rounded-lg bg-muted p-5">
            <div className="relative grid aspect-[16/9] grid-cols-[1fr_1.4fr_1fr] grid-rows-2 gap-3 rounded-md">
              {["출입구", "작업 라인 A", "적재 구역", "포장 설비", "기록 영상 미리보기"].map(
                (label, index) => (
                  <div
                    key={label}
                    className={cn(
                      "flex items-center justify-center rounded-md bg-card/70 text-sm font-medium text-muted-foreground",
                      index === 4 && "col-span-2",
                    )}
                  >
                    {label}
                  </div>
                ),
              )}
              <button
                type="button"
                aria-label="영상 재생"
                className="absolute left-1/2 top-1/2 flex size-[72px] -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg transition-transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-ring"
              >
                <Play className="ml-1 size-8" aria-hidden="true" />
              </button>
            </div>

            <div className="mt-4 rounded-lg border border-border bg-card p-3">
              <div className="flex items-center justify-between text-xs font-medium text-muted-foreground">
                <span>00:11</span>
                <span>00:30</span>
              </div>
              <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-muted">
                <div className="h-full w-[38%] rounded-full bg-primary" />
              </div>
              <div className="mt-4 flex flex-wrap items-center justify-between gap-4">
                <div className="flex flex-wrap gap-2">
                  <button className="flex h-9 items-center gap-2 rounded-md bg-muted px-3 text-sm font-medium text-foreground transition-colors hover:bg-secondary">
                    <Pause className="size-4" aria-hidden="true" />
                    일시정지
                  </button>
                  <button className="flex h-9 items-center gap-2 rounded-md bg-muted px-3 text-sm font-medium text-foreground transition-colors hover:bg-secondary">
                    <SkipBack className="size-4" aria-hidden="true" />
                    이전 5초
                  </button>
                  <button className="flex h-9 items-center gap-2 rounded-md bg-muted px-3 text-sm font-medium text-foreground transition-colors hover:bg-secondary">
                    <SkipForward className="size-4" aria-hidden="true" />
                    다음 5초
                  </button>
                </div>
                <div className="flex items-center gap-3 text-muted-foreground">
                  <Volume2 className="size-5" aria-hidden="true" />
                  <div className="h-1.5 w-20 overflow-hidden rounded-full bg-muted">
                    <div className="h-full w-[72%] rounded-full bg-accent" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="overflow-hidden rounded-lg border border-border bg-card">
          <div className="flex items-start justify-between gap-3 p-5 pb-3">
            <div>
              <h2 className="text-xl font-bold text-foreground">
                영상 파일 목록
              </h2>
              <p className="mt-2 text-sm font-medium text-muted-foreground">
                CCTV 1번 · 2025-03-12 14시대 기준 파일
              </p>
            </div>
            <span className="rounded-full bg-primary/20 px-3 py-1 text-xs font-semibold text-primary">
              총 8건
            </span>
          </div>

          <div className="max-h-[558px] space-y-2 overflow-y-auto px-5 pb-5">
            {videoRows.map((video) => (
              <button
                key={video.id}
                type="button"
                onClick={() => setSelectedVideoId(video.id)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-md border p-3 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  selectedVideoId === video.id
                    ? "border-primary bg-primary/20"
                    : "border-transparent bg-secondary hover:bg-muted",
                )}
              >
                <span className="flex size-9 shrink-0 items-center justify-center rounded-md bg-status-info-bg text-status-info-fg">
                  <FileVideo className="size-5" aria-hidden="true" />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-bold text-foreground">
                    {video.fileName}
                  </span>
                  <span className="mt-1 block text-xs font-medium text-muted-foreground">
                    녹화 시작 {video.start} · {video.status}
                  </span>
                </span>
                <span className="rounded-full bg-muted px-2.5 py-1 text-xs font-semibold text-foreground">
                  {video.duration}
                </span>
              </button>
            ))}
          </div>

          <div className="flex items-center justify-center gap-5 border-t border-border bg-card p-4 text-sm font-medium text-foreground">
            <button className="flex items-center gap-2 rounded-md px-2 py-1 transition-colors hover:bg-muted">
              <ChevronLeft className="size-4" aria-hidden="true" />
              이전
            </button>
            <button className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
              1
            </button>
            <button className="flex size-9 items-center justify-center rounded-md transition-colors hover:bg-muted">
              2
            </button>
            <button className="flex size-9 items-center justify-center rounded-md transition-colors hover:bg-muted">
              3
            </button>
            <button className="flex items-center gap-2 rounded-md px-2 py-1 transition-colors hover:bg-muted">
              다음
              <ChevronRight className="size-4" aria-hidden="true" />
            </button>
          </div>
        </section>
      </div>
    </div>
  );
}

export function DataCleanPage() {
  const [selectedCleanVideoId, setSelectedCleanVideoId] = useState(1);
  const cleanVideos = [
    {
      id: 1,
      fileName: "CCTV 1_2026-03-18_09-30-00.mp4",
      date: "2026-03-18 09:30:00",
      duration: "30초",
      frames: "24프레임 예상",
      status: "대기",
      tone: "muted",
    },
    {
      id: 2,
      fileName: "CCTV 1_2026-03-18_09-45-00.mp4",
      date: "2026-03-18 09:45:00",
      duration: "15초",
      frames: "12프레임 예상",
      status: "변환 완료",
      tone: "warning",
    },
    {
      id: 3,
      fileName: "CCTV 1_2026-03-18_10-00-00.mp4",
      date: "2026-03-18 10:00:00",
      duration: "30초",
      frames: "24프레임 예상",
      status: "모자이크 완료",
      tone: "success",
    },
    {
      id: 4,
      fileName: "CCTV 1_2026-03-18_10-15-00.mp4",
      date: "2026-03-18 10:15:00",
      duration: "30초",
      frames: "24프레임 예상",
      status: "대기",
      tone: "muted",
    },
    {
      id: 5,
      fileName: "CCTV 1_2026-03-18_10-30-00.mp4",
      date: "2026-03-18 10:30:00",
      duration: "15초",
      frames: "12프레임 예상",
      status: "대기",
      tone: "muted",
    },
  ];
  const cleanSteps = [
    {
      step: "1단계",
      title: "영상 선택",
      description: "CCTV 파일 목록에서 처리할 영상을 선택합니다.",
    },
    {
      step: "2단계",
      title: "이미지 변환",
      description: "선택한 영상을 프레임 기반 이미지로 변환합니다.",
    },
    {
      step: "3단계",
      title: "모자이크 적용",
      description: "추출된 이미지에 AI 기반 얼굴 모자이크를 적용합니다.",
    },
  ];
  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header>
        <h1 className="text-3xl font-bold text-foreground">데이터 정제</h1>
        <p className="mt-3 text-sm font-medium text-muted-foreground">
          영상 데이터를 이미지로 변환하고 AI 기반 후처리를 수행합니다.
        </p>
      </header>

      <section className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card p-4">
        <span className="text-sm font-medium text-muted-foreground">
          CCTV 선택
        </span>
        <div className="flex flex-wrap gap-2">
          {Array.from({ length: 8 }, (_, index) => `${index + 1}번`).map(
            (label, index) => (
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
            ),
          )}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[390px_1fr]">
        <section className="rounded-lg border border-border bg-card p-5">
          <h2 className="text-xl font-bold text-foreground">영상 파일 목록</h2>
          <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
            선택한 CCTV의 저장 영상 중 하나를 선택하여 프레임 추출과 모자이크 처리를 진행합니다.
          </p>

          <div className="mt-5 inline-flex items-center rounded-full bg-primary/20 px-3 py-1.5 text-sm font-semibold text-foreground">
            CCTV 1
          </div>

          <div className="mt-5 space-y-2">
            {cleanVideos.map((video) => (
              <button
                key={video.id}
                type="button"
                onClick={() => setSelectedCleanVideoId(video.id)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-md border p-4 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  selectedCleanVideoId === video.id
                    ? "border-primary bg-primary/20"
                    : "border-border bg-card hover:bg-muted",
                )}
              >
                <FileVideo className="size-5 shrink-0 text-foreground" aria-hidden="true" />
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm font-bold text-foreground">
                    {video.fileName}
                  </span>
                  <span className="mt-2 flex flex-wrap gap-5 text-xs font-medium text-muted-foreground">
                    <span>{video.date}</span>
                    <span>{video.duration}</span>
                  </span>
                  <span className="mt-2 block text-xs font-medium text-muted-foreground">
                    {video.frames}
                  </span>
                </span>
                <span
                  className={cn(
                    "shrink-0 rounded-full px-3 py-1 text-xs font-semibold",
                    video.tone === "success" &&
                      "bg-status-success-bg text-status-success-fg",
                    video.tone === "warning" &&
                      "bg-status-warning-bg text-status-warning-fg",
                    video.tone === "muted" &&
                      "bg-muted text-foreground",
                  )}
                >
                  {video.status}
                </span>
              </button>
            ))}
          </div>

          <div className="mt-5 flex items-center justify-between text-sm font-medium text-muted-foreground">
            <span>1-5 / 8건 표시</span>
            <div className="flex items-center gap-2">
              <button className="flex h-9 items-center gap-2 rounded-md border border-border px-4 text-foreground transition-colors hover:bg-muted">
                <ChevronLeft className="size-4" aria-hidden="true" /> 이전
              </button>
              <button className="flex size-9 items-center justify-center rounded-md border border-primary bg-primary/20 text-foreground">
                1
              </button>
              <button className="flex size-9 items-center justify-center rounded-md border border-border text-foreground transition-colors hover:bg-muted">
                2
              </button>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-5">
          <h2 className="text-xl font-bold text-foreground">처리 패널</h2>
          <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
            선택한 영상에 대해 단계별로 처리를 수행합니다. 자동 실행되지 않으며 사용자가 각 단계를 직접 시작합니다.
          </p>

          <div className="mt-5 inline-flex items-center gap-2 rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
            <CheckCircle2 className="size-4" aria-hidden="true" />
            대기 상태
          </div>

          <div className="mt-5 grid gap-3 lg:grid-cols-3">
            {cleanSteps.map((step, index) => (
              <button
                key={step.step}
                type="button"
                className={cn(
                  "rounded-lg border p-4 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  index === 0
                    ? "border-primary bg-primary/20"
                    : "border-border bg-card hover:bg-muted",
                )}
              >
                <p className="text-xs font-medium text-muted-foreground">
                  {step.step}
                </p>
                <h3 className="mt-4 font-bold text-foreground">{step.title}</h3>
                <p className="mt-3 text-xs font-medium leading-5 text-muted-foreground">
                  {step.description}
                </p>
              </button>
            ))}
          </div>

          <div className="mt-5 flex min-h-[358px] items-center justify-center rounded-lg border border-dashed border-border bg-card p-8 text-center">
            <div className="max-w-md">
              <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-primary/20 text-primary">
                <FileVideo className="size-7" aria-hidden="true" />
              </div>
              <h3 className="mt-7 text-xl font-bold text-foreground">
                영상 파일을 선택해주세요.
              </h3>
              <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                좌측 목록에서 영상을 선택하면 이미지 변환 버튼이 활성화되고, 처리 결과가 이 영역에 표시됩니다.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export function DataAugmentPage() {
  const [selectedAugmentVideoId, setSelectedAugmentVideoId] = useState(1);
  const augmentVideos = [
    {
      id: 1,
      fileName: "CCTV 1_2026-03-18_09-30-00",
      date: "2026-03-18 09:30:00",
      duration: "30초",
      images: "18장",
    },
    {
      id: 2,
      fileName: "CCTV 1_2026-03-18_10-10-00",
      date: "2026-03-18 10:10:00",
      duration: "15초",
      images: "9장",
    },
    {
      id: 3,
      fileName: "CCTV 1_2026-03-19_09-00-00",
      date: "2026-03-19 09:00:00",
      duration: "30초",
      images: "16장",
    },
    {
      id: 4,
      fileName: "CCTV 1_2026-03-19_11-00-00",
      date: "2026-03-19 11:00:00",
      duration: "30초",
      images: "20장",
    },
    {
      id: 5,
      fileName: "CCTV 1_2026-03-20_08-30-00",
      date: "2026-03-20 08:30:00",
      duration: "15초",
      images: "8장",
    },
  ];
  const augmentSteps = [
    {
      step: "1단계",
      title: "영상 선택",
      description: "좌측 목록에서 라벨링할 데이터 세트를 선택합니다.",
    },
    {
      step: "2단계",
      title: "이미지 선택",
      description: "썸네일을 직접 클릭하여 라벨링 대상을 고릅니다.",
    },
    {
      step: "3단계",
      title: "AI 라벨링",
      description: "선택한 이미지에 사람 탐지를 수행하고 결과를 바로 표시합니다.",
    },
  ];

  return (
    <div className="mx-auto max-w-[1144px] space-y-5">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-foreground">데이터 가공</h1>
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            정제된 이미지 데이터를 선택하고 AI 기반 자동 라벨링을 수행합니다.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex h-9 items-center gap-2 rounded-full bg-muted px-4 text-sm font-semibold text-foreground">
            <CalendarDays className="size-4" aria-hidden="true" />
            날짜별 그룹 + 썸네일 그리드
          </span>
          <button
            type="button"
            onClick={() => toast.success("자동 라벨링 더미 실행")}
            className="inline-flex h-9 items-center gap-2 rounded-full bg-primary/20 px-4 text-sm font-semibold text-foreground transition-colors hover:bg-primary/30 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <Wand2 className="size-4" aria-hidden="true" />
            선택 후 원클릭 자동 라벨링
          </button>
        </div>
      </header>

      <section className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card p-4">
        <span className="text-sm font-medium text-muted-foreground">
          CCTV 선택
        </span>
        <div className="flex flex-wrap gap-2">
          {Array.from({ length: 8 }, (_, index) => `${index + 1}번`).map(
            (label, index) => (
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
            ),
          )}
        </div>
      </section>

      <div className="grid gap-5 xl:grid-cols-[350px_1fr]">
        <section className="rounded-lg border border-border bg-card p-5">
          <h2 className="text-xl font-bold text-foreground">작업 대상 영상</h2>
          <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
            선택한 CCTV에서 정제 완료된 이미지 세트를 불러올 영상 파일을 선택합니다.
          </p>

          <div className="mt-5 inline-flex items-center rounded-full bg-primary/20 px-3 py-1.5 text-sm font-semibold text-foreground">
            CCTV 1
          </div>

          <div className="mt-5 space-y-2">
            {augmentVideos.map((video) => (
              <button
                key={video.id}
                type="button"
                onClick={() => setSelectedAugmentVideoId(video.id)}
                className={cn(
                  "flex w-full items-center gap-3 rounded-md border p-4 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  selectedAugmentVideoId === video.id
                    ? "border-primary bg-primary/20"
                    : "border-border bg-card hover:bg-muted",
                )}
              >
                <FileVideo className="size-5 shrink-0 text-foreground" aria-hidden="true" />
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
                  정제 완료
                </span>
              </button>
            ))}
          </div>

          <div className="mt-5 flex items-center justify-between text-sm font-medium text-muted-foreground">
            <span>1-5 / 7건 표시</span>
            <div className="flex items-center gap-2">
              <button className="flex h-9 items-center gap-2 rounded-md border border-border px-4 text-foreground transition-colors hover:bg-muted">
                <ChevronLeft className="size-4" aria-hidden="true" /> 이전
              </button>
              <button className="flex size-9 items-center justify-center rounded-md border border-primary bg-primary/20 text-foreground">
                1
              </button>
              <button className="flex size-9 items-center justify-center rounded-md border border-border text-foreground transition-colors hover:bg-muted">
                2
              </button>
              <button className="flex h-9 items-center gap-2 rounded-md border border-border px-4 text-foreground transition-colors hover:bg-muted">
                다음 <ChevronRight className="size-4" aria-hidden="true" />
              </button>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-5">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-bold text-foreground">
                이미지 선택 및 라벨링
              </h2>
              <p className="mt-2 text-sm font-medium leading-6 text-muted-foreground">
                날짜별로 정렬된 이미지 세트에서 필요한 데이터를 선택하고 AI 자동 라벨링을 실행합니다.
              </p>
            </div>
            <span className="inline-flex items-center gap-2 rounded-full bg-status-info-bg px-3 py-1.5 text-sm font-semibold text-status-info-fg">
              <CheckCircle2 className="size-4" aria-hidden="true" />
              대기 상태
            </span>
          </div>

          <div className="mt-5 grid gap-3 lg:grid-cols-3">
            {augmentSteps.map((step, index) => (
              <button
                key={step.step}
                type="button"
                className={cn(
                  "rounded-lg border p-4 text-left transition-colors focus:outline-none focus:ring-2 focus:ring-ring",
                  index === 0
                    ? "border-primary bg-primary/20"
                    : "border-border bg-card hover:bg-muted",
                )}
              >
                <p className="text-xs font-medium text-muted-foreground">
                  {step.step}
                </p>
                <h3 className="mt-4 font-bold text-foreground">{step.title}</h3>
                <p className="mt-3 text-xs font-medium leading-5 text-muted-foreground">
                  {step.description}
                </p>
              </button>
            ))}
          </div>

          <div className="mt-5 flex min-h-[426px] items-center justify-center rounded-lg border border-dashed border-border bg-card p-8 text-center">
            <div className="max-w-md">
              <div className="mx-auto flex size-14 items-center justify-center rounded-full bg-primary/20 text-primary">
                <ImageIcon className="size-7" aria-hidden="true" />
              </div>
              <h3 className="mt-7 text-xl font-bold text-foreground">
                영상 파일을 선택해주세요.
              </h3>
              <p className="mt-4 text-sm font-medium leading-6 text-muted-foreground">
                좌측 패널에서 영상을 선택하면 날짜별 이미지 그룹이 표시되고, 상단에서 전체 선택 후 바로 라벨링할 수 있습니다.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
