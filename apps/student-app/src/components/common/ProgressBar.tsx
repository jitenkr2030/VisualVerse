import { HTMLAttributes, forwardRef } from 'react';
import { cn } from '../../utils/cn';

interface ProgressBarProps extends HTMLAttributes<HTMLDivElement> {
  value: number;
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  variant?: 'primary' | 'success' | 'warning' | 'error';
}

const ProgressBar = forwardRef<HTMLDivElement, ProgressBarProps>(
  (
    {
      className,
      value,
      max = 100,
      size = 'md',
      showLabel = false,
      variant = 'primary',
      ...props
    },
    ref
  ) => {
    const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

    const sizes = {
      sm: 'h-1',
      md: 'h-2',
      lg: 'h-3',
    };

    const variants = {
      primary: 'bg-primary-500',
      success: 'bg-green-500',
      warning: 'bg-amber-500',
      error: 'bg-red-500',
    };

    return (
      <div className={cn('w-full', className)} {...props}>
        <div className={cn('w-full rounded-full bg-secondary-200 overflow-hidden', sizes[size])}>
          <div
            ref={ref}
            className={cn(
              'h-full rounded-full transition-all duration-500 ease-out',
              variants[variant]
            )}
            style={{ width: `${percentage}%` }}
          />
        </div>
        {showLabel && (
          <p className="mt-1 text-sm text-secondary-600 text-right">{Math.round(percentage)}%</p>
        )}
      </div>
    );
  }
);

ProgressBar.displayName = 'ProgressBar';

export default ProgressBar;
