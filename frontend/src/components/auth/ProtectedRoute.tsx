import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { LoadingScreen } from '../common/LoadingScreen';
import { useAuthStore } from '../../store/authStore';

export function ProtectedRoute() {
  const { user, isLoading } = useAuthStore();
  const location = useLocation();
  if (isLoading) return <LoadingScreen />;
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  return <Outlet />;
}
