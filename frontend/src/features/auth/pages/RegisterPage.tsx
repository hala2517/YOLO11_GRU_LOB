import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { Eye, EyeOff, Lock, ShieldCheck, User, UserPlus, Waves } from "lucide-react";
import { cn } from "@/shared/lib/utils";

export function RegisterPage() {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [form, setForm] = useState({
    loginId: "",
    password: "",
    passwordConfirm: "",
  });
  const passwordsMismatch =
    form.passwordConfirm.length > 0 && form.password !== form.passwordConfirm;
  const canSubmit =
    form.loginId.length > 0 &&
    form.password.length > 0 &&
    form.passwordConfirm.length > 0 &&
    !passwordsMismatch;

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!canSubmit) return;
    toast.success("회원가입이 완료되었습니다. 로그인해주세요.");
    navigate("/login");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <div className="w-full max-w-[440px] space-y-7">
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
          onSubmit={handleSubmit}
          className="rounded-lg border border-border bg-card px-7 py-8 shadow-sm"
        >
          <div className="text-center">
            <h2 className="text-[28px] font-bold leading-tight text-foreground">
              회원가입
            </h2>
            <p className="mt-3 text-sm font-medium text-muted-foreground">
              AIPoC 모니터링 시스템 계정을 생성하세요
            </p>
          </div>

          <div className="mt-7 space-y-[18px]">
            <div className="space-y-2">
              <label
                htmlFor="register-login-id"
                className="text-sm font-semibold text-foreground"
              >
                아이디
              </label>
              <div className="flex h-12 items-center gap-3 rounded-md border border-input bg-card px-4 text-muted-foreground focus-within:ring-2 focus-within:ring-ring">
                <User
                  className="size-5 shrink-0 text-foreground"
                  aria-hidden="true"
                />
                <input
                  id="register-login-id"
                  required
                  autoComplete="username"
                  value={form.loginId}
                  onChange={(event) =>
                    setForm((value) => ({
                      ...value,
                      loginId: event.target.value,
                    }))
                  }
                  className="h-full min-w-0 flex-1 bg-transparent text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground"
                  placeholder="아이디를 입력하세요"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label
                htmlFor="register-password"
                className="text-sm font-semibold text-foreground"
              >
                비밀번호
              </label>
              <div className="flex h-12 items-center gap-3 rounded-md border border-input bg-card px-4 text-muted-foreground focus-within:ring-2 focus-within:ring-ring">
                <Lock
                  className="size-5 shrink-0 text-foreground"
                  aria-hidden="true"
                />
                <input
                  id="register-password"
                  required
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  value={form.password}
                  onChange={(event) =>
                    setForm((value) => ({
                      ...value,
                      password: event.target.value,
                    }))
                  }
                  className="h-full min-w-0 flex-1 bg-transparent text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground"
                  placeholder="비밀번호를 입력하세요"
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
            </div>

            <div className="space-y-2">
              <label
                htmlFor="register-password-confirm"
                className="text-sm font-semibold text-foreground"
              >
                비밀번호 확인
              </label>
              <div
                className={cn(
                  "flex h-12 items-center gap-3 rounded-md border bg-card px-4 text-muted-foreground focus-within:ring-2 focus-within:ring-ring",
                  passwordsMismatch ? "border-destructive" : "border-input",
                )}
              >
                <ShieldCheck
                  className="size-5 shrink-0 text-foreground"
                  aria-hidden="true"
                />
                <input
                  id="register-password-confirm"
                  required
                  type={showPassword ? "text" : "password"}
                  autoComplete="new-password"
                  value={form.passwordConfirm}
                  onChange={(event) =>
                    setForm((value) => ({
                      ...value,
                      passwordConfirm: event.target.value,
                    }))
                  }
                  className="h-full min-w-0 flex-1 bg-transparent text-sm font-medium text-foreground outline-none placeholder:text-muted-foreground"
                  placeholder="비밀번호를 다시 입력하세요"
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
              {passwordsMismatch && (
                <p className="text-xs text-destructive">
                  비밀번호가 일치하지 않습니다.
                </p>
              )}
            </div>
          </div>

          <button
            type="submit"
            disabled={!canSubmit}
            className="mt-6 flex h-12 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          >
            <UserPlus className="size-5" aria-hidden="true" />
            회원가입
          </button>

          <div className="mt-4 flex justify-center text-sm font-medium text-muted-foreground">
            <Link
              to="/login"
              className="rounded-sm transition-colors hover:text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            >
              로그인으로 돌아가기
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
