import { useRecoilValue } from 'recoil';

import { Stack, Typography } from '@mui/material';

import LogoDark from 'assets/logo_dark.svg';
import LogoLight from 'assets/logo_light.svg';
import PDLogoDark from 'assets/pd_logo_dark.png';
import PDLogoLight from 'assets/pd_logo_light.png';

import { settingsState } from 'state/settings';

export default function WaterMark() {
  const { theme } = useRecoilValue(settingsState);
  // const src = theme === 'light' ? LogoLight : LogoDark;
  const src = theme === 'light' ? PDLogoLight : PDLogoDark;
  return (
    <Stack mx="auto">
      <a
        href="https://www.prodyna.com"
        target="_blank"
        style={{
          display: 'flex',
          alignItems: 'center',
          textDecoration: 'none'
        }}
      >
        <Typography fontSize="12px" color="text.secondary">
          Built by
        </Typography>
        <img
          src={src}
          alt="watermark"
          style={{ width: 20, filter: 'grayscale(1)', marginLeft: '4px' }}
        />
      </a>
    </Stack>
  );
}
