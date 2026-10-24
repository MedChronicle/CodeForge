import { useEffect, lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { AppShell } from './components/layout/AppShell';
import { LoadingScreen } from './components/common/LoadingScreen';
import { useAuthStore } from './store/authStore';
import { usePreferencesStore } from './store/preferencesStore';

const LandingPage = lazy(() => import('./pages/LandingPage').then((module) => ({ default: module.LandingPage })));
const LoginPage = lazy(() => import('./pages/LoginPage').then((module) => ({ default: module.LoginPage })));
const RegisterPage = lazy(() => import('./pages/RegisterPage').then((module) => ({ default: module.RegisterPage })));
const OnboardingPage = lazy(() => import('./pages/OnboardingPage').then((module) => ({ default: module.OnboardingPage })));
const DashboardPage = lazy(() => import('./pages/DashboardPage').then((module) => ({ default: module.DashboardPage })));
const SheetPage = lazy(() => import('./pages/SheetPage').then((module) => ({ default: module.SheetPage })));
const A2ZPage = lazy(() => import('./pages/A2ZPage').then((module) => ({ default: module.A2ZPage })));
const ProblemWorkspacePage = lazy(() => import('./pages/ProblemWorkspacePage').then((module) => ({ default: module.ProblemWorkspacePage })));
const ResourcesPage = lazy(() => import('./pages/ResourcesPage').then((module) => ({ default: module.ResourcesPage })));
const RevisionPage = lazy(() => import('./pages/RevisionPage').then((module) => ({ default: module.RevisionPage })));
const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage').then((module) => ({ default: module.AdminDashboardPage })));

function AppRoutes() {
  const user = useAuthStore((state) => state.user);
  const profile = useAuthStore((state) => state.profile);
  return <Suspense fallback={<LoadingScreen />}><Routes><Route path="/" element={<LandingPage />} /><Route path="/login" element={user ? <Navigate to="/app" replace /> : <LoginPage />} /><Route path="/register" element={user ? <Navigate to="/onboarding" replace /> : <RegisterPage />} /><Route element={<ProtectedRoute />}><Route path="/onboarding" element={profile?.onboarding_complete ? <Navigate to="/app" replace /> : <OnboardingPage />} /><Route path="/app" element={<AppShell><DashboardPage /></AppShell>} /><Route path="/app/sheet" element={<AppShell><SheetPage /></AppShell>} /><Route path="/app/a2z" element={<AppShell><A2ZPage /></AppShell>} /><Route path="/app/problem/:problemId" element={<AppShell><ProblemWorkspacePage /></AppShell>} /><Route path="/app/resources" element={<AppShell><ResourcesPage /></AppShell>} /><Route path="/app/revision" element={<AppShell><RevisionPage /></AppShell>} /><Route path="/app/admin" element={user?.is_admin ? <AppShell><AdminDashboardPage /></AppShell> : <Navigate to="/app" replace />} /></Route><Route path="*" element={<Navigate to="/" replace />} /></Routes></Suspense>;
}

export default function App() {
  const hydrate = useAuthStore((state) => state.hydrate);
  const theme = usePreferencesStore((state) => state.theme);
  useEffect(() => { document.documentElement.dataset.theme = theme; void hydrate(); }, [hydrate, theme]);
  return <AppRoutes />;
}
