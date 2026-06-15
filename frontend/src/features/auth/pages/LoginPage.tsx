import { useForm } from "react-hook-form";
import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { cn } from "@/shared/lib/utils";
import { setToken } from "@/shared/api/client";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Eye, EyeOff, LogIn, Lock, User, Waves } from "lucide-react";

const loginSchema = z.object({
  login_id: z.string().min(1, "아이디를 입력하세요"),
  password: z.string().min(1, "비밀번호를 입력하세요"),
});

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginPage() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = (_data: LoginFormValues) => {
    setToken("prototype-access-token");
    toast.success("프로토타입 더미 로그인 완료");
    navigate("/mornitoring/dashboard");
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <div className="w-full max-w-[420px] space-y-7">
        <div className="flex flex-col items-center text-center">
          <div className="mb-5 flex size-14 items-center justify-center rounded-lg bg-primary/20 text-accent">
            <Waves className="size-5" aria-hidden="true" />
          </div>
          <h1 className="text-[34px] font-bold leading-none text-foreground">
            COSMECCA
          </h1>
          <p className="mt-4 text-sm font-medium text-muted-foreground">
            산업 AI 모니터링 플랫폼
          </p>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="rounded-lg border border-border bg-card px-7 py-8 shadow-sm"
        >
          <div className="text-center">
            <h2 className="text-[28px] font-bold leading-tight text-foreground">
              로그인
            </h2>
            <p className="mt-3 text-sm font-medium text-muted-foreground">
              AIPoC 모니터링 시스템에 로그인하세요
            </p>
          </div>

          <div className="mt-7 space-y-[18px]">
            <div className="space-y-2">
              <label
                htmlFor="login_id"
                className="text-sm font-semibold text-foreground"
              >
                아이디
              </label>
              <div
                className={cn(
                  "flex h-12 items-center gap-3 rounded-md border bg-card px-4 text-muted-foreground focus-within:ring-2 focus-within:ring-ring",
                  errors.login_id ? "border-destructive" : "border-input",
                )}
              >
                <User
                  className="size-5 shrink-0 text-foreground"
                  aria-hidden="true"
                />
                <input
                  id="login_id"
                  type="text"
                  autoComplete="username"
                  placeholder="아이디를 입력하세요"
                  className="h-full min-w-0 flex-1 bg-transparent text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground"
                  {...register("login_id")}
                />
              </div>
              {errors.login_id && (
                <p className="text-xs text-destructive">
                  {errors.login_id.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <label
                htmlFor="password"
                className="text-sm font-semibold text-foreground"
              >
                비밀번호
              </label>
              <div
                className={cn(
                  "flex h-12 items-center gap-3 rounded-md border bg-card px-4 text-muted-foreground focus-within:ring-2 focus-within:ring-ring",
                  errors.password ? "border-destructive" : "border-input",
                )}
              >
                <Lock
                  className="size-5 shrink-0 text-foreground"
                  aria-hidden="true"
                />
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  placeholder="비밀번호를 입력하세요"
                  className="h-full min-w-0 flex-1 bg-transparent text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground"
                  {...register("password")}
                />
                <button
                  type="button"
                  aria-label={showPassword ? "비밀번호 숨기기" : "비밀번호 보기"}
                  onClick={() => setShowPassword((value) => !value)}
                  className="flex size-8 shrink-0 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                >
                  {showPassword ? (
                    <EyeOff className="size-5" aria-hidden="true" />
                  ) : (
                    <Eye className="size-5" aria-hidden="true" />
                  )}
                </button>
              </div>
              {errors.password && (
                <p className="text-xs text-destructive">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <button
            type="submit"
            className="mt-6 flex h-12 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
          >
            <LogIn className="size-5" aria-hidden="true" />
            로그인
          </button>

          <div className="mt-4 flex items-center justify-center gap-4 text-sm font-medium text-muted-foreground">
            <Link
              to="/register"
              className="rounded-sm transition-colors hover:text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              회원가입
            </Link>
            <span className="size-1 rounded-full bg-border" aria-hidden="true" />
            <Link
              to="#"
              className="rounded-sm transition-colors hover:text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              비밀번호 찾기
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
