import { Button } from '@/components/ui/button';

function CoachIcon() {
  return (
    <svg
      width="72"
      height="72"
      viewBox="0 0 72 72"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="mb-4"
    >
      {/* Speech bubble */}
      <rect
        x="10"
        y="8"
        width="52"
        height="38"
        rx="8"
        className="fill-primary/10 stroke-primary"
        strokeWidth="2.5"
      />
      {/* Bubble tail */}
      <path
        d="M22 46 L18 56 L30 46"
        className="fill-primary/10 stroke-primary"
        strokeWidth="2.5"
        strokeLinejoin="round"
      />
      {/* Microphone icon inside bubble */}
      <rect x="32" y="18" width="8" height="14" rx="4" className="fill-primary" />
      <path
        d="M28 28 C28 33.5 31.5 37 36 37 C40.5 37 44 33.5 44 28"
        className="stroke-primary"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
      />
      <line
        x1="36"
        y1="37"
        x2="36"
        y2="42"
        className="stroke-primary"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
      <line
        x1="31"
        y1="42"
        x2="41"
        y2="42"
        className="stroke-primary"
        strokeWidth="2.5"
        strokeLinecap="round"
      />
    </svg>
  );
}

function FeaturePill({ children }: { children: React.ReactNode }) {
  return (
    <span className="bg-primary/10 text-primary rounded-full px-3 py-1 text-xs font-medium">
      {children}
    </span>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center">
        <CoachIcon />

        <h1 className="text-foreground max-w-prose text-xl leading-7 font-semibold md:text-2xl">
          Meet Maya, your AI interview coach
        </h1>

        <p className="text-muted-foreground mt-2 max-w-sm text-sm leading-6">
          Practice behavioral interviews face-to-face and get real-time STAR method feedback
        </p>

        <div className="mt-4 flex flex-wrap justify-center gap-2">
          <FeaturePill>STAR Coaching</FeaturePill>
          <FeaturePill>Adaptive Difficulty</FeaturePill>
          <FeaturePill>Real-time Feedback</FeaturePill>
        </div>

        <Button
          size="lg"
          onClick={onStartCall}
          className="mt-6 w-64 rounded-full font-mono text-xs font-bold tracking-wider uppercase"
        >
          {startButtonText}
        </Button>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Tip: Speak naturally — your coach will guide you through each question.
        </p>
      </div>
    </div>
  );
};
