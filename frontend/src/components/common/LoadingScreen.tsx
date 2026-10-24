export function LoadingScreen({ label = 'Loading your forge...' }: { label?: string }) {
  return <div className="flex min-h-[40vh] items-center justify-center text-sm text-slate-400"><span className="mr-3 h-5 w-5 animate-spin rounded-full border-2 border-violet border-t-transparent" />{label}</div>;
}
