import { ImgHTMLAttributes, forwardRef } from 'react';
import { cn } from '../../utils/cn';

interface AvatarProps extends ImgHTMLAttributes<HTMLImageElement> {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  fallback?: string;
}

const Avatar = forwardRef<HTMLImageElement, AvatarProps>(
  ({ className, size = 'md', src, alt, fallback, ...props }, ref) => {
    const sizes = {
      sm: 'w-8 h-8 text-sm',
      md: 'w-10 h-10 text-base',
      lg: 'w-12 h-12 text-lg',
      xl: 'w-16 h-16 text-xl',
    };

    const initials = fallback
      ? fallback
          .split(' ')
          .map((n) => n[0])
          .join('')
          .toUpperCase()
          .slice(0, 2)
      : '';

    if (src) {
      return (
        <img
          ref={ref}
          src={src}
          alt={alt}
          className={cn(
            'rounded-full object-cover bg-primary-100',
            sizes[size],
            className
          )}
          {...props}
        />
      );
    }

    return (
      <div
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-full bg-primary-100 text-primary-600 font-semibold',
          sizes[size],
          className
        )}
        {...props}
      >
        {initials || '?'}
      </div>
    );
  }
);

Avatar.displayName = 'Avatar';

export default Avatar;
