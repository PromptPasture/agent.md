# Forms

Forms must be accessible, validated at the right level, and clear about errors before submission. Never rely on browser defaults alone.

---

## Choosing a Form Library

| Context | Preferred approach |
| --- | --- |
| React — complex forms, many fields | React Hook Form + Zod |
| React — simple 1–3 field forms | Controlled state + Zod |
| SvelteKit | Native `action` + superforms |
| Nuxt / Vue | VeeValidate + Zod |
| Remix | Native `action` + Zod |
| Astro | Native `action` or API route |

---

## React Hook Form + Zod

### Schema and types

```ts
// features/auth/login.schema.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Enter a valid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters'),
  rememberMe: z.boolean().optional().default(false),
});

export type LoginFormValues = z.infer<typeof loginSchema>;
```

### Form component

```tsx
// features/auth/LoginForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, type LoginFormValues } from './login.schema';

interface LoginFormProps {
  onSubmit: (values: LoginFormValues) => Promise<void>;
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { rememberMe: false },
  });

  async function submit(values: LoginFormValues) {
    try {
      await onSubmit(values);
    } catch {
      // Surface server errors at the field or form level
      setError('root', { message: 'Invalid email or password. Please try again.' });
    }
  }

  return (
    <form onSubmit={handleSubmit(submit)} noValidate aria-label="Log in">
      <Field label="Email" error={errors.email?.message} required>
        <input
          {...register('email')}
          type="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
      </Field>

      <Field label="Password" error={errors.password?.message} required>
        <input
          {...register('password')}
          type="password"
          autoComplete="current-password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
      </Field>

      <label>
        <input {...register('rememberMe')} type="checkbox" />
        Remember me for 30 days
      </label>

      {errors.root && (
        <div role="alert" aria-live="assertive">
          {errors.root.message}
        </div>
      )}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in…' : 'Log in'}
      </button>
    </form>
  );
}
```

### Reusable Field component

```tsx
// components/Field/Field.tsx
interface FieldProps {
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactElement;
}

export function Field({ label, error, required, children }: FieldProps) {
  const id = useId();
  const errorId = `${id}-error`;

  return (
    <div>
      <label htmlFor={id}>
        {label}
        {required && <span aria-hidden="true"> *</span>}
        {required && <span className="sr-only"> (required)</span>}
      </label>

      {cloneElement(children, { id, 'aria-describedby': error ? errorId : undefined })}

      {error && (
        <p id={errorId} role="alert" aria-live="polite">
          {error}
        </p>
      )}
    </div>
  );
}
```

---

## Validation Strategy

### Validate at the right level

| Level | When | How |
| --- | --- | --- |
| Schema (Zod) | On submit, on blur | `zodResolver` |
| Field (inline) | After first blur | RHF `mode: 'onBlur'` |
| Server | After submit | `setError('root', ...)` or field-level |
| Real-time | For confirmations only (e.g. password match) | `watch` + `validate` |

Never validate on every keystroke for standard fields — it is distracting. Validate on blur after first interaction, then on every change after the first error.

```ts
useForm({
  resolver: zodResolver(schema),
  mode: 'onBlur',          // first validation on blur
  reValidateMode: 'onChange', // re-validate on change after first error
});
```

### Server-side errors

Always map server validation errors back to specific fields when possible:

```tsx
try {
  await submitForm(values);
} catch (err) {
  if (isValidationError(err)) {
    err.fields.forEach(({ field, message }) => {
      setError(field as keyof FormValues, { message });
    });
  } else {
    setError('root', { message: 'Something went wrong. Please try again.' });
  }
}
```

---

## Accessibility

- Every input has an associated `<label>` via matching `id` and `htmlFor` — never use `placeholder` as a label
- `placeholder` is supplementary hint text only — it disappears on input and is not a substitute for a label
- Required fields: use native `required` attribute AND `aria-required="true"` for maximum compatibility
- Invalid fields: `aria-invalid="true"` on the input; `aria-describedby` pointing to the error message element
- Error messages: `role="alert"` or `aria-live="polite"` so screen readers announce them without focus moving
- Form-level errors: `role="alert"` at the top of the form, announced immediately on submit failure

```tsx
// Correct — label + aria attributes wired up
<label htmlFor="email">Email address</label>
<input
  id="email"
  type="email"
  required
  aria-required="true"
  aria-invalid={!!emailError}
  aria-describedby={emailError ? 'email-error' : undefined}
/>
{emailError && (
  <p id="email-error" role="alert">
    {emailError}
  </p>
)}
```

---

## Controlled vs Uncontrolled

Prefer **uncontrolled** (React Hook Form's `register`) for performance — no re-render on every keystroke.

Use **controlled** (`useState` + `value` + `onChange`) only when:

- The input value must drive other UI immediately (e.g. live character count, dependent field)
- Integrating a third-party input component that requires `value` and `onChange`

```tsx
// Controlled — only when necessary
const [search, setSearch] = useState('');
<input
  value={search}
  onChange={e => setSearch(e.target.value)}
  aria-label="Search"
/>
```

---

## Select, Radio, and Checkbox Groups

### Select

```tsx
<Field label="Country" error={errors.country?.message} required>
  <select {...register('country')} defaultValue="">
    <option value="" disabled>Select a country</option>
    <option value="us">United States</option>
    <option value="gb">United Kingdom</option>
  </select>
</Field>
```

### Radio group

```tsx
<fieldset>
  <legend>Subscription plan</legend>
  {plans.map(plan => (
    <label key={plan.id}>
      <input
        {...register('plan')}
        type="radio"
        value={plan.id}
      />
      {plan.name}
    </label>
  ))}
  {errors.plan && <p role="alert">{errors.plan.message}</p>}
</fieldset>
```

### Checkbox group

```tsx
<fieldset>
  <legend>Notification preferences</legend>
  {options.map(option => (
    <label key={option.id}>
      <input
        type="checkbox"
        value={option.id}
        {...register('notifications')}
      />
      {option.label}
    </label>
  ))}
</fieldset>
```

---

## File Inputs

```tsx
<Field label="Profile photo" error={errors.avatar?.message}>
  <input
    {...register('avatar')}
    type="file"
    accept="image/png, image/jpeg, image/webp"
    aria-describedby="avatar-hint"
  />
</Field>
<p id="avatar-hint">PNG, JPG, or WebP. Max 2 MB.</p>
```

Validate file type and size in the Zod schema:

```ts
avatar: z
  .instanceof(FileList)
  .refine(files => files.length > 0, 'Photo is required')
  .refine(files => files[0]?.size <= 2 * 1024 * 1024, 'Max file size is 2 MB')
  .refine(
    files => ['image/png', 'image/jpeg', 'image/webp'].includes(files[0]?.type),
    'Only PNG, JPG, or WebP allowed',
  ),
```

---

## Submit State

Always disable the submit button during submission. Restore it with an error if submission fails — never leave the user stuck.

```tsx
<button type="submit" disabled={isSubmitting} aria-busy={isSubmitting}>
  {isSubmitting ? 'Saving…' : 'Save changes'}
</button>
```

After a successful submission, give explicit confirmation — do not silently reset the form:

```tsx
if (isSubmitSuccessful) {
  return (
    <div role="status" aria-live="polite">
      <p>Your changes have been saved.</p>
      <button onClick={() => reset()}>Make another change</button>
    </div>
  );
}
```
