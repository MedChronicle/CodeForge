import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/auth/AuthLayout';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/authStore';
import { apiErrorMessage } from '../lib/utils';

export function RegisterPage() {
  const navigate = useNavigate();
  const signUp = useAuthStore((state) => state.signUp);
  const [form, setForm] = useState({ displayName: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError(''); setLoading(true);
    try { await signUp(form.email, form.password, form.displayName); navigate('/onboarding'); } catch (err) { setError(apiErrorMessage(err, 'Unable to create your account.')); } finally { setLoading(false); }
  }
  return <AuthLayout title="Build your edge." subtitle="A few honest answers. Then a practice system that meets you where you are."><form onSubmit={submit} className="space-y-5"><label className="block text-sm font-medium">Name<input required minLength={2} value={form.displayName} onChange={(event) => setForm({ ...form, displayName: event.target.value })} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.05] px-4 py-3 outline-none focus:border-violet" placeholder="Alex Morgan" /></label><label className="block text-sm font-medium">Email<input required type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.05] px-4 py-3 outline-none focus:border-violet" placeholder="you@example.com" /></label><label className="block text-sm font-medium">Password<input required minLength={8} type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.05] px-4 py-3 outline-none focus:border-violet" placeholder="At least 8 characters + a number" /></label>{error && <div className="rounded-xl border border-coral/25 bg-coral/10 p-3 text-sm text-coral">{error}</div>}<Button type="submit" loading={loading} className="w-full">Create my account</Button></form><p className="mt-7 text-center text-sm text-slate-500">Already have an account? <Link to="/login" className="font-semibold text-cyan hover:underline">Sign in</Link></p></AuthLayout>;
}
