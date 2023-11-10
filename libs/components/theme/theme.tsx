import createTheme from '@mui/material/styles/createTheme';

import { green, grey, primary, white } from './palette';

const typography = {
  fontFamily: ['Inter', 'sans-serif'].join(',')
};

const components = {
  MuiButton: {
    defaultProps: {
      disableElevation: true,
      disableRipple: true,
      sx: {
        textTransform: 'none'
      }
    }
  },
  MuiLink: {
    defaultProps: {
      fontWeight: 500
    }
  },
  MuiFormHelperText: {
    defaultProps: {
      sx: {
        m: 0,
        fontWeight: 400,
        color: grey[500]
      }
    }
  },
  MuiTooltip: {
    styleOverrides: {
      tooltip: {
        backgroundColor: 'black'
      }
    }
  }
};

const shape = {
  borderRadius: 8
};

const success = {
  main: green[500],
  contrastText: white
};
const error = {
  main: 'rgba(239, 65, 70, 1)',
  contrastText: white
};

const darkTheme = createTheme({
  typography,
  components,
  shape,
  palette: {
    mode: 'dark',
    success,
    error,
    background: {
      default: grey[850],
      paper: grey[900]
    },
    primary: {
      main: '#009ee2',
      dark: primary[800],
      light: '#ccf0ff',
      contrastText: white
    },
    secondary: {
      main: '#99e0ff',
      dark: '#006b99',
      light: '#99e0ff',
      contrastText: white
    },
    divider: grey[800],
    text: {
      primary: grey[200],
      secondary: grey[400]
    }
  }
});

const lightTheme = createTheme({
  typography,
  components,
  shape,
  palette: {
    mode: 'light',
    success,
    error,
    background: {
      default: grey[50],
      paper: white
    },
    primary: {
      main: '#009ee2',
      dark: primary[800],
      light: '#ccf0ff',
      contrastText: white
    },
    secondary: {
      main: '#99e0ff',
      dark: '#006b99',
      light: '#99e0ff',
      contrastText: white
    },
    divider: grey[200],
    text: {
      primary: grey[900],
      secondary: grey[700]
    }
  }
});

const makeTheme = (variant: 'dark' | 'light') =>
  variant === 'dark' ? darkTheme : lightTheme;

const darkGreyButtonTheme = createTheme({
  typography,
  components,
  shape,
  palette: {
    primary: {
      main: grey[900]
    }
  }
});

const lightGreyButtonTheme = createTheme({
  typography,
  components,
  shape,
  palette: {
    primary: {
      main: grey[200]
    }
  }
});

// Maybe we should not export dark and light theme button from the package
export { makeTheme, darkGreyButtonTheme, lightGreyButtonTheme };
