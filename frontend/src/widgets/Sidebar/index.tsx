import type { ReactNode } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  BarChart3,
  Bot,
  Box,
  ChevronDown,
  Database,
  ListChecks,
  Shield,
} from "lucide-react";
import { cn } from "@/shared/lib/utils";

interface NavChild {
  label: string;
  to: string;
}

interface NavGroup {
  label: string;
  icon: ReactNode;
  items: NavChild[];
}

const NAV_GROUPS: NavGroup[] = [
  {
    label: "데이터 수집",
    icon: <Database className="size-4" aria-hidden="true" />,
    items: [
      { label: "데이터 수집 환경", to: "/data-collection/env" },
      { label: "데이터 수집", to: "/data-collection/jobs" },
      { label: "데이터 정제", to: "/data-collection/clean" },
      { label: "데이터 가공", to: "/data-collection/augment" },
    ],
  },
  {
    label: "데이터 분석",
    icon: <BarChart3 className="size-4" aria-hidden="true" />,
    items: [{ label: "데이터 검수", to: "/data-inspection" }],
  },
  {
    label: "AI 모델링",
    icon: <Bot className="size-4" aria-hidden="true" />,
    items: [
      { label: "AI 모델 학습", to: "/ai/training" },
      { label: "모델 평가 결과", to: "/ai/evaluation" },
    ],
  },
  {
    label: "서비스",
    icon: <Shield className="size-4" aria-hidden="true" />,
    items: [
      { label: "작업현장 모니터링", to: "/mornitoring/dashboard" },
      { label: "비인가자 접근 알림서비스", to: "/alerts/unauthorized" },
      { label: "이벤트 이력 관리", to: "/alerts/history" },
      { label: "작업자 동선 관리", to: "/worker-flow" },
      { label: "MES 연동", to: "/mes-integration" },
    ],
  },
];

function isGroupActive(pathname: string, group: NavGroup) {
  if (group.items.some((item) => pathname === item.to)) return true;
  return pathname.startsWith("/mornitoring/") && group.label === "서비스";
}

export function Sidebar() {
  const { pathname } = useLocation();

  return (
    <aside className="flex h-screen w-60 shrink-0 flex-col border-r border-sidebar-border bg-sidebar-background text-sidebar-foreground">
      <div className="flex h-16 items-center gap-3 border-b border-sidebar-border px-6">
        <Box className="size-5 text-sidebar-primary" aria-hidden="true" />
        <span className="text-xl font-bold tracking-normal text-sidebar-foreground">
          AIPoC 모니터링
        </span>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-6">
        <div className="space-y-3">
          {NAV_GROUPS.map((group) => {
            const groupActive = isGroupActive(pathname, group);
            return (
              <details
                key={group.label}
                className="group"
                open={groupActive || group.label === "서비스"}
              >
                <summary
                  className={cn(
                    "flex h-11 cursor-pointer list-none items-center gap-3 rounded-md px-3 text-sm font-bold transition-colors marker:hidden",
                    groupActive
                      ? "bg-sidebar-accent text-sidebar-primary"
                      : "text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                  )}
                >
                  {group.icon}
                  <span className="min-w-0 flex-1">{group.label}</span>
                  <ChevronDown
                    className="size-4 text-sidebar-foreground/70 transition-transform group-open:rotate-180"
                    aria-hidden="true"
                  />
                </summary>

                <div className="mt-2 space-y-1 pl-8">
                  {group.items.map((item) => (
                    <NavLink
                      key={item.to}
                      to={item.to}
                      className={({ isActive }) =>
                        cn(
                          "flex h-10 items-center rounded-md px-3 text-sm font-medium transition-colors",
                          isActive
                            ? "bg-primary/20 text-sidebar-foreground"
                            : "text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
                        )
                      }
                    >
                      <ListChecks
                        className="mr-2 size-3.5 opacity-0"
                        aria-hidden="true"
                      />
                      <span className="truncate">{item.label}</span>
                    </NavLink>
                  ))}
                </div>
              </details>
            );
          })}
        </div>
      </nav>

      <div className="border-t border-sidebar-border px-6 py-4">
        <div className="flex items-center gap-3 rounded-md bg-sidebar-accent px-3 py-3">
          <div className="flex size-9 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
            홍
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-bold text-sidebar-foreground">
              홍길동님
            </p>
            <p className="truncate text-xs font-medium text-sidebar-foreground/60">
              생산기술팀
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
