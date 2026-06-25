# Forms

Forms must be accessible, validated at the right level, and clear about errors before submission. Don't rely on browser defaults.

---

## Validation Strategy

### Validate at the right level

|Level|When|Purpose|
|---|---|---|
|Schema|On submit, on blur|Catch type and format errors|
|Field|After first blur, then on change|Immediate feedback after interaction|
|Server|After submit|Business rules, uniqueness, auth|
|Real-time|Confirmations only (e.g. password match)|Dependent field checks|

Never validate on every keystroke for standard fields — it is distracting. Validate on blur after first interaction, then on every change once the first error has appeared.

### Server-side errors

Always map server validation errors back to specific fields when possible. A generic form-level error is the fallback, not the default.

```
On validation error from server:
  Field-specific error → show beside the field
  General error        → show at the top of the form in a role="alert" region
```

---

## Accessibility

Every form must meet these requirements — no exceptions:

- Every input has an associated `<label>` via matching `for` / `id` — never use `placeholder` as a label
- `placeholder` is supplementary hint text only — it disappears on input and conveys nothing to screen readers
- Required fields use native `required` — `aria-required="true"` is only needed on custom controls that cannot use the native attribute
- Invalid fields: `aria-invalid="true"` on the input; `aria-describedby` pointing to the error element
- Error messages use `role="alert"` or `aria-live="polite"` so screen readers announce them without moving focus
- Form-level errors use `role="alert"` and appear at the top of the form — announced immediately on submit failure

```html
<label for="email">Email address</label>
<input
  id="email"
  type="email"
  required
  aria-invalid="true"
  aria-describedby="email-error"
/>
<p id="email-error" role="alert">Enter a valid email address</p>
```

---

## Controlled vs Uncontrolled Inputs

Prefer **uncontrolled inputs** (DOM-managed via form libraries) for performance — no re-render on every keystroke.

Use **controlled inputs** (value bound to reactive state) only when:

- The value must drive other UI immediately (live character count, dependent field visibility)
- A third-party input component requires a bound value

---

## Input Groups

### Select

```html
<label for="country">Country</label>
<select id="country" name="country" required>
  <option value="" disabled selected>Select a country</option>
  <option value="us">United States</option>
  <option value="gb">United Kingdom</option>
</select>
```

### Radio group — always use fieldset + legend

```html
<fieldset>
  <legend>Subscription plan</legend>
  <label><input type="radio" name="plan" value="free" /> Free</label>
  <label><input type="radio" name="plan" value="pro" /> Pro</label>
</fieldset>
```

### Checkbox group — always use fieldset + legend

```html
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="checkbox" name="notifications" value="email" /> Email</label>
  <label><input type="checkbox" name="notifications" value="sms" /> SMS</label>
</fieldset>
```

---

## File Inputs

```html
<label for="avatar">Profile photo</label>
<input
  id="avatar"
  type="file"
  name="avatar"
  accept="image/png, image/jpeg, image/webp"
  aria-describedby="avatar-hint"
/>
<p id="avatar-hint">PNG, JPG, or WebP. Max 2 MB.</p>
```

Validate file type and size on both client and server:

```
Client validation:
  file.size  <= 2 * 1024 * 1024         (2 MB)
  file.type  in ['image/png', 'image/jpeg', 'image/webp']

Server validation:
  Re-validate — never trust client-side checks alone
```

---

## Submit State

Always disable the submit button during submission. Use `aria-busy` to announce the pending state to screen readers. Restore with an error on failure — never leave the user stuck.

```html
<!-- Pending -->
<button type="submit" disabled aria-busy="true">Saving…</button>

<!-- Default -->
<button type="submit">Save changes</button>
```

After a successful submission, give explicit confirmation — do not silently reset the form:

```html
<div role="status" aria-live="polite">
  <p>Your changes have been saved.</p>
  <button type="button">Make another change</button>
</div>
```
