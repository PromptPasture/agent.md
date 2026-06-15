# Angular — Framework Adapter

Angular is a full-featured, opinionated TypeScript framework with built-in dependency injection, reactive forms, and RxJS. Uses class-based components with decorators. Angular 17+ introduces Signals for fine-grained reactivity alongside RxJS.

---

## Conventions

### File extensions

- `.component.ts` + `.component.html` + `.component.scss` — component class, template, styles
- `.service.ts` — injectable services
- `.directive.ts` — custom directives
- `.pipe.ts` — template pipes
- `.guard.ts` — route guards
- `.interceptor.ts` — HTTP interceptors
- `.spec.ts` — unit tests (co-located)

### Component structure

```ts
// user-card.component.ts
import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import type { User } from '@/app/models/user.model';

@Component({
  selector: 'app-user-card',
  standalone: true,               // Angular 14+ — prefer standalone over NgModules
  imports: [CommonModule],
  templateUrl: './user-card.component.html',
  styleUrl: './user-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush, // always use OnPush
})
export class UserCardComponent {
  @Input({ required: true }) user!: User;
  @Input() featured = false;
  @Output() selected = new EventEmitter<string>();

  onSelect() {
    this.selected.emit(this.user.id);
  }
}
```

```html
<!-- user-card.component.html -->
<article class="user-card" [class.featured]="featured" (click)="onSelect()">
  <span class="name">{{ user.name }}</span>
  <span class="role">{{ user.role }}</span>
</article>
```

### Naming conventions

| Thing | Convention | Example |
| --- | --- | --- |
| Component selector | `app-` prefix, kebab-case | `app-user-card` |
| Class name | PascalCase + suffix | `UserCardComponent` |
| Service | PascalCase + `Service` | `UserService` |
| Interface/model | PascalCase | `User`, `ApiResponse` |
| File | kebab-case + `.type.ts` | `user-card.component.ts` |

---

## Error Handling

### Global error handler

```ts
// app/core/global-error-handler.ts
import { ErrorHandler, Injectable, inject } from '@angular/core';
import { LoggingService } from './logging.service';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  private logging = inject(LoggingService);

  handleError(error: unknown): void {
    this.logging.logError(error);
    console.error('Unhandled error:', error);
  }
}

// app.config.ts
providers: [{ provide: ErrorHandler, useClass: GlobalErrorHandler }]
```

### HTTP error interceptor

```ts
// core/http-error.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';

export const httpErrorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) router.navigate(['/login']);
      if (error.status === 403) router.navigate(['/forbidden']);
      return throwError(() => error);
    })
  );
};
```

### Component error states

```ts
@Component({ template: `
  @if (isLoading) { <app-skeleton /> }
  @else if (error) { <app-error-message [message]="error" (retry)="load()" /> }
  @else { <app-user-profile [user]="user!" /> }
` })
export class UserProfilePage {
  user: User | null = null;
  isLoading = true;
  error: string | null = null;

  constructor(private userService: UserService) {}

  ngOnInit() { this.load(); }

  load() {
    this.isLoading = true;
    this.error = null;
    this.userService.getUser(this.id).subscribe({
      next:  user  => { this.user = user; this.isLoading = false; },
      error: err   => { this.error = err.message; this.isLoading = false; },
    });
  }
}
```

---

## Motion

Angular does not bundle an animation library. Use Angular Animations (built-in, based on Web Animations API) or CSS transitions.

```ts
// Angular Animations
import { trigger, state, style, animate, transition } from '@angular/animations';

@Component({
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(12px)' }),
        animate('200ms ease-out', style({ opacity: 1, transform: 'translateY(0)' })),
      ]),
      transition(':leave', [
        animate('150ms ease-in', style({ opacity: 0 })),
      ]),
    ]),
  ],
  template: `<div @fadeIn *ngIf="visible">Content</div>`,
})
export class AnimatedComponent {
  visible = true;
}
```

Always respect `prefers-reduced-motion` — see `references/motion.md`.

---

## Accessibility

Angular CDK provides accessible primitives (focus trap, live announcer, overlay).

```ts
import { FocusTrap, FocusTrapFactory } from '@angular/cdk/a11y';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({})
export class DialogComponent implements OnInit, OnDestroy {
  private focusTrap?: FocusTrap;

  constructor(
    private el: ElementRef,
    private focusTrapFactory: FocusTrapFactory,
    private announcer: LiveAnnouncer,
  ) {}

  ngOnInit() {
    this.focusTrap = this.focusTrapFactory.create(this.el.nativeElement);
    this.focusTrap.focusInitialElement();
    this.announcer.announce('Dialog opened', 'polite');
  }

  ngOnDestroy() {
    this.focusTrap?.destroy();
  }
}
```

---

## Performance

### OnPush change detection — always

```ts
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush, // on every component
})
```

OnPush only re-renders when:

- An `@Input` reference changes
- An event originates from the component
- An `async` pipe emits
- `markForCheck()` is called manually

### trackBy for ngFor

```html
<li *ngFor="let item of items; trackBy: trackById">{{ item.name }}</li>
```

```ts
trackById(index: number, item: Item): string { return item.id; }
```

### Lazy-load routes

```ts
// app.routes.ts
export const routes: Routes = [
  { path: 'dashboard', loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent) },
  { path: 'admin',     loadChildren: () => import('./admin/admin.routes').then(m => m.ADMIN_ROUTES) },
];
```

---

## Data Fetching — HttpClient

```ts
// core/api.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = '/api';

  get<T>(path: string): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}${path}`).pipe(
      catchError(this.handleError)
    );
  }

  post<T>(path: string, body: unknown): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}${path}`, body).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    const message = error.error?.message ?? error.message;
    return throwError(() => new Error(message));
  }
}
```

### Signals + resource (Angular 19+)

```ts
import { resource, signal } from '@angular/core';

export class UserComponent {
  userId = signal('123');

  userResource = resource({
    request: () => ({ id: this.userId() }),
    loader: ({ request }) => fetch(`/api/users/${request.id}`).then(r => r.json()),
  });

  // userResource.value() — data
  // userResource.isLoading() — loading state
  // userResource.error() — error
}
```

---

## Forms — Reactive Forms

Always prefer Reactive Forms over Template-driven Forms for complex or validated forms.

```ts
// login.component.ts
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <label for="email">Email</label>
      <input id="email" formControlName="email" type="email"
        [attr.aria-invalid]="isInvalid('email')"
        [attr.aria-describedby]="isInvalid('email') ? 'email-error' : null" />
      @if (isInvalid('email')) {
        <p id="email-error" role="alert">
          {{ form.get('email')?.hasError('required') ? 'Required' : 'Invalid email' }}
        </p>
      }

      <button type="submit" [disabled]="form.invalid || isSubmitting">
        {{ isSubmitting ? 'Logging in…' : 'Log in' }}
      </button>
      @if (serverError) { <div role="alert">{{ serverError }}</div> }
    </form>
  `,
})
export class LoginComponent {
  private fb = inject(FormBuilder);
  isSubmitting = false;
  serverError: string | null = null;

  form = this.fb.group({
    email:    ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(8)]],
  });

  isInvalid(field: string): boolean {
    const control = this.form.get(field);
    return !!(control?.invalid && control.touched);
  }

  async submit() {
    if (this.form.invalid) { this.form.markAllAsTouched(); return; }
    this.isSubmitting = true;
    this.serverError = null;
    try {
      await this.authService.login(this.form.value as LoginInput);
    } catch (err) {
      this.serverError = err instanceof Error ? err.message : 'Something went wrong';
    } finally {
      this.isSubmitting = false;
    }
  }
}
```

---

## State

### Signals (Angular 17+) — preferred for local and shared state

```ts
import { signal, computed, effect } from '@angular/core';

// Local state
const count  = signal(0);
const double = computed(() => count() * 2);

effect(() => { console.log('Count changed:', count()); });

// Update
count.set(5);
count.update(prev => prev + 1);
```

### Service + BehaviorSubject (RxJS pattern)

```ts
@Injectable({ providedIn: 'root' })
export class CartService {
  private items$ = new BehaviorSubject<CartItem[]>([]);

  readonly items  = this.items$.asObservable();
  readonly total$ = this.items$.pipe(
    map(items => items.reduce((sum, i) => sum + i.price * i.quantity, 0))
  );

  addItem(item: CartItem) {
    this.items$.next([...this.items$.value, item]);
  }
}
```

### NgRx — for large apps requiring devtools and strict unidirectional flow

```ts
// actions
export const loadUsers = createAction('[Users] Load');
export const loadUsersSuccess = createAction('[Users] Load Success', props<{ users: User[] }>());

// reducer
export const usersReducer = createReducer(
  initialState,
  on(loadUsersSuccess, (state, { users }) => ({ ...state, users, loading: false }))
);

// selector
export const selectUsers = createSelector(selectUsersState, state => state.users);
```

---

## SEO — Angular SSR / Universal

```ts
// Install: ng add @angular/ssr
// app.config.server.ts is generated automatically

// In components, use Meta and Title services
import { Meta, Title } from '@angular/platform-browser';

@Component({})
export class ProductPage {
  constructor(private title: Title, private meta: Meta) {}

  ngOnInit() {
    this.title.setTitle(`${this.product.name} — MyApp`);
    this.meta.updateTag({ name: 'description', content: this.product.description });
    this.meta.updateTag({ property: 'og:title', content: this.product.name });
    this.meta.updateTag({ property: 'og:image', content: this.product.imageUrl });
  }
}
```

---

## PWA

```bash
ng add @angular/pwa
```

This adds `ngsw-config.json`, registers the service worker, and configures Workbox automatically.

```json
// ngsw-config.json
{
  "dataGroups": [
    {
      "name": "api-freshness",
      "urls": ["/api/**"],
      "cacheConfig": { "strategy": "freshness", "maxSize": 100, "maxAge": "1d" }
    }
  ]
}
```

---

## i18n

### Built-in Angular i18n

```ts
// angular.json — add locales
"i18n": {
  "sourceLocale": "en",
  "locales": { "fr": "src/locale/messages.fr.xlf" }
}
```

```html
<!-- Mark strings for extraction -->
<h1 i18n="Site title">Welcome to MyApp</h1>
<p i18n>Items in cart: {{ count }}</p>
```

```bash
ng extract-i18n        # extract messages.xlf
ng build --localize    # build for all locales
```

### ngx-translate (runtime, no build step per locale)

```ts
// app.config.ts
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';

TranslateModule.forRoot({
  loader: { provide: TranslateLoader, useFactory: createTranslateLoader, deps: [HttpClient] },
  defaultLanguage: 'en',
})
```

```html
{{ 'product.addToCart' | translate }}
{{ 'cart.items' | translate: { count: cartCount } }}
```
