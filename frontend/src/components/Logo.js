import React from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const LogoContainer = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'variant',
})(({ variant }) => ({
  display: 'flex',
  flexDirection: variant === 'horizontal' ? 'row' : 'column',
  alignItems: 'center',
  gap: variant === 'horizontal' ? 8 : 4,
  height: variant === 'horizontal' ? '100%' : 'auto',
  justifyContent: 'center',
  textAlign: 'center',
}));

const LogoImage = styled('img')(({ size }) => ({
  height: size || 'auto',
  width: 'auto',
  maxWidth: '100%',
  objectFit: 'contain',
}));

const Logo = ({ size = 'medium', variant = 'horizontal' }) => {
  const sizes = {
    small: { height: 40, text: 'h6' },
    medium: { height: 60, text: 'h5' },
    large: { height: 100, text: 'h3' },
  };

  const { height, text } = sizes[size] || sizes.medium;
  const isSmall = size === 'small';

  return (
    <LogoContainer variant={variant}>
      <LogoImage 
        src="/Hy-Classe_Group_LOGO_copie-removebg-preview.png" 
        alt="Hy-Classe Group Logo"
        size={height}
      />
      {!isSmall && variant === 'vertical' && (
        <Box sx={{ textAlign: 'center' }}>
          <Typography 
            variant="caption" 
            component="div" 
            sx={{ 
              fontWeight: 500,
              color: 'text.secondary',
              lineHeight: 1.2,
              fontSize: '0.75rem',
              mt: 0.5,
            }}
          >
            Powered by
          </Typography>
          <Typography 
            component="div" 
            sx={{ 
              fontWeight: 600,
              color: 'primary.main',
              lineHeight: 1.2,
              fontSize: '0.8rem',
              letterSpacing: '0.5px',
            }}
          >
            AFOSE WORKS
          </Typography>
        </Box>
      )}
      {!isSmall && variant === 'horizontal' && (
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column',
          justifyContent: 'center',
          height: '100%',
          paddingTop: '4px',
        }}>
          <Typography 
            variant="caption" 
            component="div" 
            sx={{ 
              fontWeight: 500,
              color: 'text.secondary',
              lineHeight: 1.2,
              fontSize: '0.7rem',
            }}
          >
            Powered by
          </Typography>
          <Typography 
            component="div" 
            sx={{ 
              fontWeight: 600,
              color: 'primary.main',
              lineHeight: 1.2,
              fontSize: '0.75rem',
              letterSpacing: '0.5px',
            }}
          >
            AFOSE WORKS
          </Typography>
        </Box>
      )}
    </LogoContainer>
  );
};

export default Logo;
