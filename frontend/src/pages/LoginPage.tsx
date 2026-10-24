import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/auth/AuthLayout';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/authStore';
import { apiErrorMessage } from '../lib/utils';

export function LoginPage() {
  const navigate = useNavigate();
  const signIn = useAuthStore((state) => state.signIn);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError(''); setLoading(true);
    try { await signIn(email, password); navigate('/app'); } catch (err) { setError(apiErrorMessage(err, 'Unable to sign in. Check your details.')); } finally { setLoading(false); }
  }
  return <AuthLayout title="Welcome back." subtitle="Pick up exactly where your momentum left off."><form onSubmit={submit} className="space-y-5"><label className="block text-sm font-medium">Email<input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.05] px-4 py-3 outline-none transition focus:border-violet" placeholder="you@example.com" /></label><label className="block text-sm font-medium">Password<input required type="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.05] px-4 py-3 outline-none transition focus:border-violet" placeholder="••••••••" /></label>{error && <div className="rounded-xl border border-coral/25 bg-coral/10 p-3 text-sm text-coral">{error}</div>}<Button type="submit" loading={loading} className="w-full">Enter the forge</Button></form><p className="mt-7 text-center text-sm text-slate-500">New here? <Link to="/register" className="font-semibold text-cyan hover:underline">Create your sheet</Link></p></AuthLayout>;
}
