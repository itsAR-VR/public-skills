import * as React from "react";

type ClassValue = string | false | null | undefined;

export function cn(...values: ClassValue[]) {
  return values.filter(Boolean).join(" ");
}

export type Action = {
  label: string;
  href?: string;
  icon?: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost";
  onClick?: () => void;
};

export type NavItem = {
  label: string;
  href?: string;
  icon?: React.ReactNode;
  active?: boolean;
  badge?: string;
  onClick?: () => void;
};

const actionStyles = {
  primary:
    "bg-neutral-950 text-white shadow-sm hover:bg-neutral-800 focus-visible:ring-neutral-950",
  secondary:
    "border border-neutral-200 bg-white text-neutral-950 shadow-sm hover:bg-neutral-50 focus-visible:ring-neutral-300",
  ghost:
    "text-neutral-700 hover:bg-neutral-100 hover:text-neutral-950 focus-visible:ring-neutral-300",
};

export function ActionButton({
  action,
  className,
}: {
  action: Action;
  className?: string;
}) {
  const variant = action.variant ?? "secondary";
  const classes = cn(
    "inline-flex min-h-11 items-center justify-center gap-2 rounded-lg px-4 text-sm font-medium transition",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    actionStyles[variant],
    className,
  );

  if (action.href) {
    return (
      <a href={action.href} onClick={action.onClick} className={classes}>
        {action.icon}
        {action.label}
      </a>
    );
  }

  return (
    <button type="button" onClick={action.onClick} className={classes}>
      {action.icon}
      {action.label}
    </button>
  );
}

export function ProductAppShell({
  brand,
  navItems,
  actions,
  userSlot,
  sidebarSlot,
  children,
}: {
  brand: React.ReactNode;
  navItems: NavItem[];
  actions?: React.ReactNode;
  userSlot?: React.ReactNode;
  sidebarSlot?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-dvh bg-neutral-50 text-neutral-950">
      <div className="grid min-h-dvh lg:grid-cols-[280px_1fr]">
        <aside className="hidden border-r border-neutral-200 bg-white/85 px-4 py-4 backdrop-blur lg:block">
          <div className="mb-6 flex min-h-11 items-center">{brand}</div>
          <nav className="space-y-1" aria-label="Primary">
            {navItems.map((item) => (
              item.href ? (
                <a
                  key={item.label}
                  href={item.href}
                  onClick={item.onClick}
                  aria-current={item.active ? "page" : undefined}
                  className={cn(
                    "flex min-h-10 items-center gap-3 rounded-lg px-3 text-sm font-medium transition",
                    item.active
                      ? "bg-neutral-950 text-white shadow-sm"
                      : "text-neutral-600 hover:bg-neutral-100 hover:text-neutral-950",
                  )}
                >
                  {item.icon}
                  <span className="flex-1 truncate">{item.label}</span>
                  {item.badge ? (
                    <span className="rounded-full bg-neutral-100 px-2 py-0.5 text-xs text-neutral-600">
                      {item.badge}
                    </span>
                  ) : null}
                </a>
              ) : (
                <button
                  key={item.label}
                  type="button"
                  onClick={item.onClick}
                  aria-current={item.active ? "page" : undefined}
                  className={cn(
                    "flex w-full min-h-10 items-center gap-3 rounded-lg px-3 text-left text-sm font-medium transition",
                    item.active
                      ? "bg-neutral-950 text-white shadow-sm"
                      : "text-neutral-600 hover:bg-neutral-100 hover:text-neutral-950",
                  )}
                >
                  {item.icon}
                  <span className="flex-1 truncate">{item.label}</span>
                  {item.badge ? (
                    <span className="rounded-full bg-neutral-100 px-2 py-0.5 text-xs text-neutral-600">
                      {item.badge}
                    </span>
                  ) : null}
                </button>
              )
            ))}
          </nav>
          {sidebarSlot ? <div className="mt-6">{sidebarSlot}</div> : null}
        </aside>

        <main className="min-w-0">
          <header className="sticky top-0 z-20 border-b border-neutral-200 bg-neutral-50/85 px-4 py-3 backdrop-blur md:px-6">
            <div className="flex min-h-11 items-center justify-between gap-3">
              <div className="min-w-0 lg:hidden">{brand}</div>
              <div className="hidden min-w-0 text-sm text-neutral-500 lg:block">
                Work surface
              </div>
              <div className="flex items-center gap-2">
                {actions}
                {userSlot}
              </div>
            </div>
          </header>
          <div className="mx-auto w-full max-w-7xl px-4 py-6 md:px-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

export function LandingHero({
  eyebrow,
  title,
  description,
  actions,
  visual,
  proof,
}: {
  eyebrow?: React.ReactNode;
  title: React.ReactNode;
  description: React.ReactNode;
  actions?: Action[];
  visual?: React.ReactNode;
  proof?: React.ReactNode;
}) {
  return (
    <section className="relative overflow-hidden bg-white">
      <div className="mx-auto grid min-h-[min(760px,calc(100dvh-40px))] max-w-7xl content-center gap-10 px-4 py-16 md:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:py-24">
        <div className="max-w-3xl">
          {eyebrow ? (
            <div className="mb-5 inline-flex rounded-full border border-neutral-200 bg-neutral-50 px-3 py-1 text-sm font-medium text-neutral-600">
              {eyebrow}
            </div>
          ) : null}
          <h1 className="text-4xl font-semibold tracking-normal text-neutral-950 sm:text-5xl lg:text-6xl">
            {title}
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-neutral-600">
            {description}
          </p>
          {actions?.length ? (
            <div className="mt-8 flex flex-wrap gap-3">
              {actions.map((action) => (
                <ActionButton key={action.label} action={action} />
              ))}
            </div>
          ) : null}
          {proof ? <div className="mt-8 text-sm text-neutral-500">{proof}</div> : null}
        </div>
        {visual ? (
          <div className="min-h-[320px] overflow-hidden rounded-2xl border border-neutral-200 bg-neutral-50 shadow-sm">
            {visual}
          </div>
        ) : null}
      </div>
    </section>
  );
}

export type WizardStep = {
  id: string;
  title: string;
  description?: string;
  content: React.ReactNode;
};

export function OnboardingWizard({
  steps,
  currentStep,
  onStepChange,
  footer,
}: {
  steps: WizardStep[];
  currentStep: string;
  onStepChange?: (stepId: string) => void;
  footer?: React.ReactNode;
}) {
  const activeIndex = Math.max(
    0,
    steps.findIndex((step) => step.id === currentStep),
  );
  const activeStep = steps[activeIndex] ?? steps[0];

  if (!activeStep) {
    return (
      <div className="rounded-2xl border border-neutral-200 bg-white p-4 shadow-sm md:p-6">
        <EmptyState
          title="No steps available"
          description="There are no onboarding steps to display right now."
        />
        {footer ? <div className="mt-6 border-t border-neutral-200 pt-4">{footer}</div> : null}
      </div>
    );
  }

  return (
    <div className="grid gap-6 rounded-2xl border border-neutral-200 bg-white p-4 shadow-sm md:grid-cols-[280px_1fr] md:p-6">
      <ol className="space-y-2" aria-label="Onboarding steps">
        {steps.map((step, index) => {
          const isActive = step.id === activeStep.id;
          const isComplete = index < activeIndex;
          return (
            <li key={step.id}>
              <button
                type="button"
                onClick={() => onStepChange?.(step.id)}
                className={cn(
                  "flex w-full gap-3 rounded-xl p-3 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-300",
                  isActive ? "bg-neutral-950 text-white" : "hover:bg-neutral-50",
                )}
              >
                <span
                  className={cn(
                    "grid h-7 w-7 shrink-0 place-items-center rounded-full border text-xs font-semibold",
                    isActive
                      ? "border-white/30 bg-white text-neutral-950"
                      : isComplete
                        ? "border-neutral-950 bg-neutral-950 text-white"
                        : "border-neutral-200 text-neutral-500",
                  )}
                >
                  {index + 1}
                </span>
                <span className="min-w-0">
                  <span className="block text-sm font-semibold">{step.title}</span>
                  {step.description ? (
                    <span
                      className={cn(
                        "mt-1 block text-sm",
                        isActive ? "text-white/70" : "text-neutral-500",
                      )}
                    >
                      {step.description}
                    </span>
                  ) : null}
                </span>
              </button>
            </li>
          );
        })}
      </ol>
      <section className="min-w-0">
        <div>{activeStep.content}</div>
        {footer ? <div className="mt-6 border-t border-neutral-200 pt-4">{footer}</div> : null}
      </section>
    </div>
  );
}

export type CommandItem = {
  id: string;
  label: string;
  description?: string;
  shortcut?: string;
  icon?: React.ReactNode;
  onSelect: () => void;
};

export function CommandPalette({
  open,
  onOpenChange,
  commands,
  title = "Command menu",
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  commands: CommandItem[];
  title?: string;
}) {
  const [query, setQuery] = React.useState("");
  const filtered = commands.filter((command) =>
    `${command.label} ${command.description ?? ""}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  );

  React.useEffect(() => {
    if (!open) return;
    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") onOpenChange(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onOpenChange]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/30 p-4 backdrop-blur-sm"
      role="presentation"
      onClick={() => onOpenChange(false)}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        onClick={(event) => event.stopPropagation()}
        className="mx-auto mt-20 max-w-2xl overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-2xl"
      >
        <div className="border-b border-neutral-200 p-3">
          <input
            autoFocus
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search actions..."
            className="h-11 w-full rounded-lg border border-neutral-200 px-3 text-sm outline-none focus:border-neutral-400 focus:ring-2 focus:ring-neutral-200"
          />
        </div>
        <div className="max-h-[420px] overflow-y-auto p-2">
          {filtered.length ? (
            filtered.map((command) => (
              <button
                key={command.id}
                type="button"
                onClick={() => {
                  command.onSelect();
                  onOpenChange(false);
                }}
                className="flex w-full items-center gap-3 rounded-xl p-3 text-left transition hover:bg-neutral-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-300"
              >
                {command.icon ? (
                  <span className="grid h-9 w-9 place-items-center rounded-lg bg-neutral-100">
                    {command.icon}
                  </span>
                ) : null}
                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-semibold text-neutral-950">
                    {command.label}
                  </span>
                  {command.description ? (
                    <span className="mt-0.5 block text-sm text-neutral-500">
                      {command.description}
                    </span>
                  ) : null}
                </span>
                {command.shortcut ? (
                  <kbd className="rounded-md border border-neutral-200 bg-neutral-50 px-2 py-1 text-xs text-neutral-500">
                    {command.shortcut}
                  </kbd>
                ) : null}
              </button>
            ))
          ) : (
            <EmptyState
              title="No matching actions"
              description="Try a different search term or clear the command query."
            />
          )}
        </div>
      </div>
    </div>
  );
}

export function SlideSheet({
  open,
  onOpenChange,
  title,
  description,
  children,
  footer,
  side = "right",
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
  side?: "right" | "left";
}) {
  const sheetId = React.useId();
  const titleId = `${sheetId}-title`;
  const descriptionId = `${sheetId}-description`;

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50">
      <button
        type="button"
        aria-label="Close panel"
        className="absolute inset-0 bg-black/30 backdrop-blur-sm"
        onClick={() => onOpenChange(false)}
      />
      <aside
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={description ? descriptionId : undefined}
        className={cn(
          "absolute top-0 h-full w-full max-w-md border-neutral-200 bg-white shadow-2xl",
          side === "right" ? "right-0 border-l" : "left-0 border-r",
        )}
      >
        <div className="flex h-full flex-col">
          <header className="border-b border-neutral-200 p-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <h2 id={titleId} className="text-lg font-semibold text-neutral-950">
                  {title}
                </h2>
                {description ? (
                  <p id={descriptionId} className="mt-1 text-sm leading-6 text-neutral-500">
                    {description}
                  </p>
                ) : null}
              </div>
              <button
                type="button"
                onClick={() => onOpenChange(false)}
                className="grid h-9 w-9 place-items-center rounded-lg text-neutral-500 transition hover:bg-neutral-100 hover:text-neutral-950 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-300"
              >
                <span aria-hidden="true">x</span>
                <span className="sr-only">Close</span>
              </button>
            </div>
          </header>
          <div className="min-h-0 flex-1 overflow-y-auto p-5">{children}</div>
          {footer ? <footer className="border-t border-neutral-200 p-5">{footer}</footer> : null}
        </div>
      </aside>
    </div>
  );
}

export function PremiumCard({
  title,
  description,
  action,
  children,
  footer,
  className,
}: {
  title?: React.ReactNode;
  description?: React.ReactNode;
  action?: React.ReactNode;
  children?: React.ReactNode;
  footer?: React.ReactNode;
  className?: string;
}) {
  return (
    <section
      className={cn(
        "rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm",
        "supports-[backdrop-filter]:bg-white/85 supports-[backdrop-filter]:backdrop-blur",
        className,
      )}
    >
      {(title || description || action) && (
        <div className="mb-5 flex items-start justify-between gap-4">
          <div className="min-w-0">
            {title ? <h3 className="text-base font-semibold text-neutral-950">{title}</h3> : null}
            {description ? (
              <p className="mt-1 text-sm leading-6 text-neutral-500">{description}</p>
            ) : null}
          </div>
          {action}
        </div>
      )}
      {children}
      {footer ? <div className="mt-5 border-t border-neutral-200 pt-4">{footer}</div> : null}
    </section>
  );
}

export function FieldState({
  id,
  label,
  hint,
  error,
  children,
}: {
  id: string;
  label: string;
  hint?: string;
  error?: string;
  children: React.ReactElement<{
    id?: string;
    className?: string;
    "aria-invalid"?: boolean;
    "aria-describedby"?: string;
  }>;
}) {
  const describedBy = error ? `${id}-error` : hint ? `${id}-hint` : undefined;
  return (
    <div className="space-y-2">
      <label htmlFor={id} className="text-sm font-medium text-neutral-900">
        {label}
      </label>
      {React.cloneElement(children, {
        id,
        "aria-invalid": Boolean(error),
        "aria-describedby": describedBy,
        className: cn(
          "h-11 w-full rounded-lg border bg-white px-3 text-sm outline-none transition placeholder:text-neutral-400",
          error
            ? "border-red-300 focus:border-red-400 focus:ring-2 focus:ring-red-100"
            : "border-neutral-200 focus:border-neutral-400 focus:ring-2 focus:ring-neutral-200",
          children.props.className,
        ),
      })}
      {error ? (
        <p id={`${id}-error`} className="text-sm text-red-600">
          {error}
        </p>
      ) : hint ? (
        <p id={`${id}-hint`} className="text-sm text-neutral-500">
          {hint}
        </p>
      ) : null}
    </div>
  );
}

export function SkeletonBlock({
  className,
  label = "Loading",
}: {
  className?: string;
  label?: string;
}) {
  return (
    <div
      role="status"
      aria-label={label}
      className={cn("animate-pulse rounded-xl bg-neutral-200/80", className)}
    />
  );
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: React.ReactNode;
  description?: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <div className="grid min-h-48 place-items-center rounded-xl border border-dashed border-neutral-200 bg-neutral-50 p-8 text-center">
      <div className="max-w-sm">
        <h3 className="text-base font-semibold text-neutral-950">{title}</h3>
        {description ? (
          <p className="mt-2 text-sm leading-6 text-neutral-500">{description}</p>
        ) : null}
        {action ? <div className="mt-5">{action}</div> : null}
      </div>
    </div>
  );
}

export type ToolbarAction = {
  label: string;
  onClick?: () => void;
  variant?: Action["variant"];
};

export function DataTableFrame({
  title,
  description,
  toolbar,
  filters,
  table,
  footer,
  state,
}: {
  title: React.ReactNode;
  description?: React.ReactNode;
  toolbar?: ToolbarAction[];
  filters?: React.ReactNode;
  table: React.ReactNode;
  footer?: React.ReactNode;
  state?: React.ReactNode;
}) {
  return (
    <section className="overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm">
      <header className="flex flex-col gap-4 border-b border-neutral-200 p-5 md:flex-row md:items-start md:justify-between">
        <div className="min-w-0">
          <h2 className="text-lg font-semibold text-neutral-950">{title}</h2>
          {description ? (
            <p className="mt-1 text-sm leading-6 text-neutral-500">{description}</p>
          ) : null}
        </div>
        {toolbar?.length ? (
          <div className="flex flex-wrap gap-2">
            {toolbar.map((action) => (
              <ActionButton
                key={action.label}
                action={{ label: action.label, onClick: action.onClick, variant: action.variant }}
                className="min-h-10 px-3"
              />
            ))}
          </div>
        ) : null}
      </header>
      {filters ? <div className="border-b border-neutral-200 p-4">{filters}</div> : null}
      {state ? (
        <div className="p-5">{state}</div>
      ) : (
        <div className="w-full overflow-x-auto">{table}</div>
      )}
      {footer ? <footer className="border-t border-neutral-200 p-4">{footer}</footer> : null}
    </section>
  );
}

export function AgentWorkspace({
  title,
  description,
  thread,
  composer,
  sidePanel,
  status,
}: {
  title: React.ReactNode;
  description?: React.ReactNode;
  thread: React.ReactNode;
  composer: React.ReactNode;
  sidePanel?: React.ReactNode;
  status?: React.ReactNode;
}) {
  return (
    <section className="grid min-h-[640px] overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm lg:grid-cols-[minmax(0,1fr)_360px]">
      <div className="flex min-w-0 flex-col">
        <header className="border-b border-neutral-200 p-5">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <h2 className="text-lg font-semibold text-neutral-950">{title}</h2>
              {description ? (
                <p className="mt-1 text-sm leading-6 text-neutral-500">{description}</p>
              ) : null}
            </div>
            {status ? <div className="shrink-0">{status}</div> : null}
          </div>
        </header>
        <div className="min-h-0 flex-1 overflow-y-auto bg-neutral-50 p-4 md:p-6">{thread}</div>
        <footer className="border-t border-neutral-200 bg-white p-4">{composer}</footer>
      </div>
      {sidePanel ? (
        <aside className="border-t border-neutral-200 bg-neutral-50 p-5 lg:border-l lg:border-t-0">
          {sidePanel}
        </aside>
      ) : null}
    </section>
  );
}

export function CheckoutSummary({
  title,
  items,
  totals,
  action,
  trust,
}: {
  title: React.ReactNode;
  items: React.ReactNode;
  totals: React.ReactNode;
  action?: React.ReactNode;
  trust?: React.ReactNode;
}) {
  return (
    <aside className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-neutral-950">{title}</h2>
      <div className="mt-5 border-y border-neutral-200 py-4">{items}</div>
      <div className="mt-4">{totals}</div>
      {action ? <div className="mt-5">{action}</div> : null}
      {trust ? <div className="mt-4 text-sm leading-6 text-neutral-500">{trust}</div> : null}
    </aside>
  );
}

export function CalendarPlanner({
  title,
  controls,
  calendar,
  agenda,
  details,
}: {
  title: React.ReactNode;
  controls?: React.ReactNode;
  calendar: React.ReactNode;
  agenda?: React.ReactNode;
  details?: React.ReactNode;
}) {
  return (
    <section className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
      <div className="overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm">
        <header className="flex flex-col gap-3 border-b border-neutral-200 p-5 md:flex-row md:items-center md:justify-between">
          <h2 className="text-lg font-semibold text-neutral-950">{title}</h2>
          {controls}
        </header>
        <div className="min-h-[460px] p-4">{calendar}</div>
      </div>
      <aside className="space-y-4">
        {agenda ? (
          <section className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
            {agenda}
          </section>
        ) : null}
        {details ? (
          <section className="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
            {details}
          </section>
        ) : null}
      </aside>
    </section>
  );
}

export function EditorWorkspace({
  title,
  toolbar,
  navigation,
  editor,
  inspector,
  status,
}: {
  title: React.ReactNode;
  toolbar?: React.ReactNode;
  navigation?: React.ReactNode;
  editor: React.ReactNode;
  inspector?: React.ReactNode;
  status?: React.ReactNode;
}) {
  return (
    <section className="grid min-h-[680px] overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm lg:grid-cols-[260px_minmax(0,1fr)_320px]">
      {navigation ? (
        <aside className="hidden border-r border-neutral-200 bg-neutral-50 p-4 lg:block">
          {navigation}
        </aside>
      ) : null}
      <main className="min-w-0">
        <header className="border-b border-neutral-200 p-4">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div className="min-w-0">
              <h2 className="truncate text-lg font-semibold text-neutral-950">{title}</h2>
              {status ? <div className="mt-1 text-sm text-neutral-500">{status}</div> : null}
            </div>
            {toolbar}
          </div>
        </header>
        <div className="min-h-[560px] p-5">{editor}</div>
      </main>
      {inspector ? (
        <aside className="border-t border-neutral-200 bg-neutral-50 p-4 lg:border-l lg:border-t-0">
          {inspector}
        </aside>
      ) : null}
    </section>
  );
}

export function WorkflowCanvas({
  toolbar,
  canvas,
  inspector,
  status,
  empty,
}: {
  toolbar?: React.ReactNode;
  canvas: React.ReactNode;
  inspector?: React.ReactNode;
  status?: React.ReactNode;
  empty?: React.ReactNode;
}) {
  return (
    <section className="grid min-h-[680px] overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm lg:grid-cols-[minmax(0,1fr)_340px]">
      <main className="relative min-w-0 bg-neutral-50">
        {toolbar ? (
          <div className="absolute left-4 top-4 z-10 rounded-xl border border-neutral-200 bg-white/90 p-2 shadow-sm backdrop-blur">
            {toolbar}
          </div>
        ) : null}
        {status ? (
          <div className="absolute bottom-4 left-4 z-10 rounded-full border border-neutral-200 bg-white px-3 py-1 text-sm text-neutral-500 shadow-sm">
            {status}
          </div>
        ) : null}
        <div className="h-full min-h-[680px]">{empty ?? canvas}</div>
      </main>
      {inspector ? (
        <aside className="border-t border-neutral-200 bg-white p-5 lg:border-l lg:border-t-0">
          {inspector}
        </aside>
      ) : null}
    </section>
  );
}

export type PipelineColumn = {
  id: string;
  title: React.ReactNode;
  count?: number;
  items: React.ReactNode;
};

export function KanbanPipeline({
  columns,
  toolbar,
  empty,
}: {
  columns: PipelineColumn[];
  toolbar?: React.ReactNode;
  empty?: React.ReactNode;
}) {
  if (!columns.length) {
    return empty ? <>{empty}</> : <EmptyState title="No columns" />;
  }

  return (
    <section className="rounded-2xl border border-neutral-200 bg-neutral-50 p-4 shadow-sm">
      {toolbar ? <div className="mb-4">{toolbar}</div> : null}
      <div className="grid gap-4 overflow-x-auto md:auto-cols-[minmax(260px,1fr)] md:grid-flow-col">
        {columns.map((column) => (
          <section key={column.id} className="min-w-64 rounded-xl border border-neutral-200 bg-white">
            <header className="flex items-center justify-between gap-3 border-b border-neutral-200 p-3">
              <h3 className="text-sm font-semibold text-neutral-950">{column.title}</h3>
              {typeof column.count === "number" ? (
                <span className="rounded-full bg-neutral-100 px-2 py-0.5 text-xs text-neutral-500">
                  {column.count}
                </span>
              ) : null}
            </header>
            <div className="space-y-3 p-3">{column.items}</div>
          </section>
        ))}
      </div>
    </section>
  );
}

export function FileDropzone({
  title,
  description,
  action,
  files,
  state,
}: {
  title: React.ReactNode;
  description?: React.ReactNode;
  action?: React.ReactNode;
  files?: React.ReactNode;
  state?: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-dashed border-neutral-300 bg-white p-6 text-center shadow-sm">
      <div className="mx-auto max-w-lg">
        <h2 className="text-base font-semibold text-neutral-950">{title}</h2>
        {description ? (
          <p className="mt-2 text-sm leading-6 text-neutral-500">{description}</p>
        ) : null}
        {action ? <div className="mt-5">{action}</div> : null}
      </div>
      {state ? <div className="mt-5">{state}</div> : null}
      {files ? <div className="mt-6 text-left">{files}</div> : null}
    </section>
  );
}

export type BillingPlan = {
  id: string;
  name: React.ReactNode;
  price: React.ReactNode;
  description?: React.ReactNode;
  features?: React.ReactNode;
  action?: React.ReactNode;
  highlighted?: boolean;
};

export function BillingPlanGrid({ plans }: { plans: BillingPlan[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      {plans.map((plan) => (
        <section
          key={plan.id}
          className={cn(
            "rounded-2xl border bg-white p-5 shadow-sm",
            plan.highlighted ? "border-neutral-950 ring-2 ring-neutral-950/10" : "border-neutral-200",
          )}
        >
          <h3 className="text-base font-semibold text-neutral-950">{plan.name}</h3>
          <div className="mt-3 text-3xl font-semibold text-neutral-950">{plan.price}</div>
          {plan.description ? (
            <p className="mt-2 text-sm leading-6 text-neutral-500">{plan.description}</p>
          ) : null}
          {plan.features ? <div className="mt-5">{plan.features}</div> : null}
          {plan.action ? <div className="mt-6">{plan.action}</div> : null}
        </section>
      ))}
    </div>
  );
}

export type TimelineItem = {
  id: string;
  title: React.ReactNode;
  description?: React.ReactNode;
  time?: React.ReactNode;
  marker?: React.ReactNode;
};

export function ActivityTimeline({ items }: { items: TimelineItem[] }) {
  if (!items.length) {
    return <EmptyState title="No activity yet" description="Important updates will appear here." />;
  }

  return (
    <ol className="space-y-4">
      {items.map((item) => (
        <li key={item.id} className="grid grid-cols-[32px_1fr] gap-3">
          <div className="flex justify-center">
            <span className="mt-1 grid h-6 w-6 place-items-center rounded-full bg-neutral-900 text-xs text-white">
              {item.marker ?? ""}
            </span>
          </div>
          <div className="min-w-0 rounded-xl border border-neutral-200 bg-white p-4 shadow-sm">
            <div className="flex items-start justify-between gap-3">
              <h3 className="text-sm font-semibold text-neutral-950">{item.title}</h3>
              {item.time ? <span className="shrink-0 text-xs text-neutral-400">{item.time}</span> : null}
            </div>
            {item.description ? (
              <p className="mt-1 text-sm leading-6 text-neutral-500">{item.description}</p>
            ) : null}
          </div>
        </li>
      ))}
    </ol>
  );
}
