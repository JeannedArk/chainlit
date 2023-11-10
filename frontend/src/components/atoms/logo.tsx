import { httpEndpoint } from 'api';
import { useRecoilValue } from 'recoil';

import { settingsState } from 'state/settings';
import PDLogoLight from '../../assets/pd_logo_light.png';
import PDLogoDark from '../../assets/pd_logo_dark.png';
import AKBLogo from '../../assets/akblogo.png';
import AKBLogoBig from '../../assets/akblogobig.png';
import AKBLogoBigCropped from '../../assets/akblogobigcropped.png';

interface Props {
  width?: number;
  style?: React.CSSProperties;
}

export const Logo = ({ style }: Props) => {
  const { theme } = useRecoilValue(settingsState);
  const src = AKBLogoBigCropped;

  return (
    <img src={src} alt="logo" style={style} />
    // <img src={`${httpEndpoint}/logo?theme=${theme}`} alt="logo" style={style} />
  );
};
