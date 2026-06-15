# MUI (Material UI)

React-only. No official Svelte or Vue port exists — use shadcn-svelte or Melt UI for SvelteKit.

---

## Setup

```bash
npm install @mui/material @emotion/react @emotion/styled
# Icons (optional)
npm install @mui/icons-material
```

### Next.js — App Router requires a registry

```tsx
// src/lib/mui-registry.tsx
'use client';
import { useServerInsertedHTML } from 'next/navigation';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { useState } from 'react';

export function MuiRegistry({ children }: { children: React.ReactNode }) {
  const [registry] = useState(() => {
    const cache = createCache({ key: 'css' });
    cache.compat = true;
    return { cache };
  });

  useServerInsertedHTML(() => (
    <style
      data-emotion={`${registry.cache.key} ${Object.keys(registry.cache.inserted).join(' ')}`}
      dangerouslySetInnerHTML={{
        __html: Object.values(registry.cache.inserted).join(''),
      }}
    />
  ));

  return <CacheProvider value={registry.cache}>{children}</CacheProvider>;
}
```

```tsx
// app/layout.tsx
import { MuiRegistry } from '@/lib/mui-registry';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <MuiRegistry>{children}</MuiRegistry>
      </body>
    </html>
  );
}
```

---

## Theming

Always define a custom theme — never rely on MUI defaults in production:

```ts
// src/lib/theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary:   { main: '#6366f1' },
    secondary: { main: '#ec4899' },
    error:     { main: '#dc2626' },
  },
  typography: {
    fontFamily: '"Inter", system-ui, sans-serif',
    h1: { fontSize: '2rem',   fontWeight: 700 },
    h2: { fontSize: '1.5rem', fontWeight: 600 },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      defaultProps: { disableElevation: true },
      styleOverrides: {
        root: { textTransform: 'none', fontWeight: 500 },
      },
    },
    MuiTextField: {
      defaultProps: { variant: 'outlined', size: 'small' },
    },
  },
});
```

```tsx
// Wrap the app
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

<ThemeProvider theme={theme}>
  <CssBaseline />
  {children}
</ThemeProvider>
```

---

## styled() vs sx

**Prefer `styled()` for reusable overrides** — it creates a named component, plays well with devtools, and does not recalculate on every render.

**Use `sx` only for one-off, non-reusable adjustments.**

```tsx
import { styled } from '@mui/material/styles';
import { Button, Card } from '@mui/material';

// Good — styled() for reusable overrides
const StyledCard = styled(Card)(({ theme }) => ({
  padding:      theme.spacing(3),
  borderRadius: theme.shape.borderRadius * 2,
  boxShadow:    theme.shadows[2],
}));

// Acceptable — sx for a single one-off spacing adjustment
<Button sx={{ mt: 2 }} variant="contained">Submit</Button>

// Bad — sx for complex styling that will be reused
<Card sx={{ p: 3, borderRadius: 2, boxShadow: 2, '&:hover': { boxShadow: 4 } }}>
```

---

## Component Usage

```tsx
import {
  Box, Stack, Grid, Typography,
  Button, IconButton, TextField,
  CircularProgress, Skeleton,
  Snackbar, Alert, Dialog, DialogTitle, DialogContent, DialogActions,
} from '@mui/material';

// Layout
<Box sx={{ display: 'flex', gap: 2 }}>
<Stack spacing={2} direction="row" alignItems="center">
<Grid container spacing={2}>
  <Grid item xs={12} md={6}><Component /></Grid>
</Grid>

// Typography
<Typography variant="h2" component="h1">Title</Typography>
<Typography variant="body2" color="text.secondary">Muted text</Typography>

// Form
<TextField label="Email" type="email" required fullWidth error={!!error} helperText={error} />

// Feedback
<CircularProgress size={20} aria-label="Loading" />
<Skeleton variant="rectangular" width="100%" height={200} />

// Dialog
<Dialog open={isOpen} onClose={onClose} aria-labelledby="dialog-title">
  <DialogTitle id="dialog-title">Confirm</DialogTitle>
  <DialogContent>Are you sure?</DialogContent>
  <DialogActions>
    <Button onClick={onClose}>Cancel</Button>
    <Button onClick={onConfirm} variant="contained">Confirm</Button>
  </DialogActions>
</Dialog>
```

---

## Dark Mode

```ts
// theme.ts
export const lightTheme = createTheme({ palette: { mode: 'light', primary: { main: '#6366f1' } } });
export const darkTheme  = createTheme({ palette: { mode: 'dark',  primary: { main: '#818cf8' } } });
```

```tsx
// Toggle based on stored preference — see references/styling.md for system/light/dark logic
<ThemeProvider theme={isDark ? darkTheme : lightTheme}>
```
