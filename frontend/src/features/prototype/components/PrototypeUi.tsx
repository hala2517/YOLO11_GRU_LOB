import type { ReactNode } from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
} from "recharts";
import { cn } from "@/shared/lib/utils";

const chartColors = {
  primary: "var(--primary)",
  accent: "var(--accent)",
  success: "var(--status-success-fg)",
  warning: "var(--status-warning-fg)",
  error: "var(--status-error-fg)",
  muted: "var(--status-muted-fg)",
};

export function SectionCard({
  title,
  description,
  action,
  children,
  className,
}: {
  title?: string;
  description?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={cn(
        "rounded-xl border border-border bg-card p-5 shadow-sm",
        className,
      )}
    >
      {(title || description || action) && (
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            {title && (
              <h3 className="font-semibold text-foreground">{title}</h3>
            )}
            {description && (
              <p className="mt-1 text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}

export function MetricCard({
  title,
  value,
  hint,
  tone = "default",
}: {
  title: string;
  value: string | number;
  hint?: string;
  tone?: "default" | "success" | "warning" | "danger";
}) {
  const toneClass = {
    default: "text-primary",
    success: "text-status-success-fg",
    warning: "text-status-warning-fg",
    danger: "text-status-error-fg",
  }[tone];

  return (
    <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
      <p className="text-sm text-muted-foreground">{title}</p>
      <p className={cn("mt-2 text-2xl font-bold", toneClass)}>{value}</p>
      {hint && <p className="mt-1 text-xs text-muted-foreground">{hint}</p>}
    </div>
  );
}

export function FilterBar({ children }: { children: ReactNode }) {
  return (
    <div className="flex flex-wrap items-center gap-2 rounded-xl border border-border bg-card p-3">
      {children}
    </div>
  );
}

export function SelectBox({
  value,
  onChange,
  options,
}: {
  value: string;
  onChange: (value: string) => void;
  options: string[];
}) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
    >
      {options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}

export function Button({
  children,
  onClick,
  variant = "primary",
  type = "button",
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "danger";
  type?: "button" | "submit";
}) {
  const variantClass = {
    primary: "bg-primary text-primary-foreground hover:opacity-90",
    secondary:
      "border border-border bg-background text-foreground hover:bg-accent",
    danger: "bg-destructive text-destructive-foreground hover:opacity-90",
  }[variant];

  return (
    <button
      type={type}
      onClick={onClick}
      className={cn(
        "rounded-md px-3 py-2 text-sm font-medium transition",
        variantClass,
      )}
    >
      {children}
    </button>
  );
}

export function EmptyState({
  title,
  description,
}: {
  title: string;
  description?: string;
}) {
  return (
    <div className="rounded-lg border border-dashed border-border p-8 text-center">
      <p className="font-medium text-foreground">{title}</p>
      {description && (
        <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      )}
    </div>
  );
}

export function ProgressBar({ value }: { value: number }) {
  return (
    <div className="h-2 overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-primary"
        style={{ width: `${value}%` }}
      />
    </div>
  );
}

export function MockAreaChart({
  data,
  keys = ["worker", "helmet"],
}: {
  data: Record<string, unknown>[];
  keys?: string[];
}) {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data}>
          <XAxis dataKey="name" stroke="currentColor" fontSize={12} />
          <YAxis stroke="currentColor" fontSize={12} />
          <Tooltip />
          {keys.map((key, index) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stroke={
                index === 0
                  ? chartColors.primary
                  : index === 1
                    ? chartColors.success
                    : chartColors.error
              }
              fill={
                index === 0
                  ? "rgb(59 130 246 / 0.2)"
                  : index === 1
                    ? "rgb(34 197 94 / 0.18)"
                    : "rgb(239 68 68 / 0.14)"
              }
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MockBarChart({
  data,
  dataKey = "efficiency",
}: {
  data: Record<string, unknown>[];
  dataKey?: string;
}) {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="currentColor" fontSize={12} />
          <YAxis stroke="currentColor" fontSize={12} />
          <Tooltip />
          <Bar
            dataKey={dataKey}
            fill={chartColors.primary}
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MockPieChart() {
  const data = [
    { name: "online", value: 6 },
    { name: "warning", value: 2 },
    { name: "offline", value: 1 },
  ];
  const colors = [chartColors.success, chartColors.warning, chartColors.muted];
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            outerRadius={80}
            label
          >
            {data.map((entry, index) => (
              <Cell key={entry.name} fill={colors[index]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MockRadarChart({ data }: { data: Record<string, unknown>[] }) {
  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="metric" />
          <Radar
            dataKey="value"
            stroke={chartColors.primary}
            fill={chartColors.primary}
            fillOpacity={0.35}
          />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
