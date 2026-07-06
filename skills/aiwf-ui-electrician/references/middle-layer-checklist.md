# Middle-Layer Checklist

Use this checklist when the UI says one thing, the backend logs say another, or user actions do not map cleanly to runtime state.

## API Contract

- Request payload field names match backend models and frontend builders.
- Aliases, casing, defaults, and enum values are identical across Python and TypeScript.
- Response objects have stable keys for status, progress, result paths, warnings, and errors.
- Error responses are normalized into user-visible messages.
- Generated client types, hand-written types, and runtime normalizers agree.

## Progress And Jobs

- Each generation has a job id or equivalent active-run token.
- Phase text and overall progress come from the same job state source.
- Progress can represent loading, encoding, denoising/decoding, saving, and completed/failed/canceled terminal states.
- Polling or streaming stops only after a terminal state.
- Old jobs cannot overwrite the current job after a second generation starts.

## Cancellation And Sequential Runs

- Generate turns into Stop while a run is active.
- Stop sends the active job id or known cancel token.
- Canceled and failed jobs clean active state.
- A second generation can start after success, failure, or cancellation.
- Duplicate submits are blocked only while the intended active run is alive.

## Telemetry

- Resource usage endpoints are mounted, reachable, and refreshed on a predictable cadence.
- GPU utilization is distinct from allocated or reserved VRAM.
- UI labels match backend fields.
- Failed telemetry fetches are surfaced or degraded without permanently stopping refresh.
- Volatile telemetry fetches use `cache: "no-store"` only when caching can plausibly return stale data.

## Logs And Errors

- Backend route exceptions become structured responses.
- Frontend displays actionable status, not only console output.
- Terminal logs include route, model, backend, phase, and failure reason for generation paths.
- Client-log endpoints are mounted and actually called from the frontend.
- Toasts/status panels are not overwritten by generic polling text before users can read the error.

## File And Media Paths

- Upload controls exist for every mode that needs input media.
- Static/output URLs resolve in the browser from a fresh session.
- Output thumbnails and full-size previews point to the same completed artifact.
- Download links use the saved artifact path, not an in-memory preview path.
- Missing files show a clear error instead of an empty image/video frame.

## Settings And Launch

- Default launch mode matches the product decision.
- Flags opt out of defaults rather than being required for the expected app mode.
- App window, icon, tray label, and browser/app shell behavior are owned by launcher code, not only docs.
- Settings persistence does not override a newly selected model or backend with stale state.

## Verification

- API tests cover payload and response shape.
- Frontend build passes after type changes.
- No-GPU endpoint probes cover route availability and error surfaces.
- Live smoke tests are reserved for paths that require real runtime evidence.
