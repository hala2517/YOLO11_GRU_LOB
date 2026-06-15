export function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">대시보드</h2>
        <p className="text-sm text-muted-foreground">현장 운영 현황 요약</p>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: '현장 수', value: '-' },
          { label: '활성 카메라', value: '-' },
          { label: '미확인 알림', value: '-' },
          { label: 'AI 모델', value: '-' },
        ].map((stat) => (
          <div key={stat.label} className="rounded-lg border border-border bg-card p-4 shadow-sm">
            <p className="text-xs text-muted-foreground">{stat.label}</p>
            <p className="mt-1 text-2xl font-bold text-foreground">{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
