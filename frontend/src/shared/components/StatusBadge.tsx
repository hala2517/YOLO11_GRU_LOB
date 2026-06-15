import { cn } from "@/shared/lib/utils";
import type { DeviceStatus } from "@/entities/types";
import type { AlertSeverity } from "@/entities/types";

interface StatusBadgeProps {
  status: DeviceStatus | AlertSeverity | string;
  className?: string;
}

const deviceStatusConfig: Record<
  DeviceStatus,
  { label: string; className: string }
> = {
  online: {
    label: "온라인",
    className: "bg-status-success-bg text-status-success-fg",
  },
  offline: {
    label: "오프라인",
    className: "bg-status-muted-bg text-status-muted-fg",
  },
  error: {
    label: "오류",
    className: "bg-status-error-bg text-status-error-fg",
  },
  maintenance: {
    label: "점검",
    className: "bg-status-warning-bg text-status-warning-fg",
  },
};

const severityConfig: Record<
  AlertSeverity,
  { label: string; className: string }
> = {
  low: { label: "낮음", className: "bg-status-info-bg text-status-info-fg" },
  medium: {
    label: "보통",
    className: "bg-status-warning-bg text-status-warning-fg",
  },
  high: { label: "높음", className: "bg-status-error-bg text-status-error-fg" },
  critical: {
    label: "긴급",
    className: "bg-status-error-bg text-status-error-fg",
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = deviceStatusConfig[status as DeviceStatus] ??
    severityConfig[status as AlertSeverity] ?? {
      label: status,
      className: "bg-status-muted-bg text-status-muted-fg",
    };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        config.className,
        className,
      )}
    >
      {config.label}
    </span>
  );
}
