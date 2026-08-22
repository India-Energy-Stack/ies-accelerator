# Proposal — re-home IES domain-schema authoring (review open item O-10)

**Status:** proposal for IES + Beckn/DEG governance review. **No schema, `$id`, or URL is changed
by this document or by this branch.** This is the plan to take to both governance bodies; nothing
here is self-executing.

**Origin:** the standards-conformance review of the IES Accelerator Guide found citation errors in
the `EnergyResource`/`ElectricityCredential` DER fields, and traced them to the fact that the
schemas carrying IES domain-standards citations are authored in `beckn/DEG` and either mirrored
verbatim into `ies-accelerator` (with an explicit "don't edit in place" policy) or not vendored at
all — `EnergyResource`/`EnergyResourceCommon` exist only as `$ref`s to `schema.beckn.io`, inlined
at build time. The review's recommendation: IES-authored documents should cite IES-owned sources.
This proposal is the concrete "how."

## 1. The governing principle

Split by what gate **G1** of the review already established: Beckn/DEG's legitimate role is
**transaction coordination** (discovery, ordering, fulfillment, contracts, marketplace mechanics),
not **domain-standards semantics** (what a field means physically, which IEC/IEEE/BIS/CEA standard
governs it). Schemas doing the former stay with Beckn/DEG; schemas doing the latter move to IES.
This isn't a land-grab — it draws the ownership boundary at the same line the review already used
to judge correctness.

## 2. Concrete scope (from a full inventory of the current repo, 2026-07-04)

| Bucket | Schema families | Disposition |
|---|---|---|
|**A — moves to IES**|`EnergyResource`, `EnergyResourceCommon` (currently `$ref`-only, never vendored — these carry every citation this review corrected)|Re-home now. Highest priority: this is where the actual conformance errors lived.|
|**A — moves to IES**|`ElectricityCredential` (v1.0, v1.1, v1.2 — currently a verbatim DEG mirror)|Re-home now. IES already treats this as its primary credential artifact; the mirror policy is the exact thing blocking durable fixes.|
|**B — stays with Beckn/DEG**|`DEGContract`, `DemandFlexBuyOffer`, `DemandFlexNeed`, `DemandFlexPerformance`, `EnergyTradeOffer`, `P2PTrade`, `RevenueFlow`, `EnergyOrderItem`|No change. These are transaction/marketplace mechanics — squarely Beckn/DEG's coordination role, not domain-standards content.|
|**C — shared utility, needs its own review**|`CustomerDetails`, `IdRef`, `MeterServiceProfile`, `EnergyCredential` (base), `EnergyCustomer(Profile)`, `Address`, `GeoJSONGeometry`, `Location`, `BecknTimeSeries`, `ConsumptionProfileCredential`, `GenerationProfileCredential`, `StorageProfileCredential`|Not decided here. These are referenced by both domain (A) and coordination (B) schemas — moving them affects both sides. Recommend a second, narrower proposal once A is settled.|
|**D — already IES-native**|`ArrFiling`, `MeterData`, `MeterDataCredential`, `MeterDataRequest`, `MeterDataRequestCredential`, `OutageNotification`|No change needed — these already have no mirror banner and are authored directly in `ies-accelerator`.|

**Phase 1 of this proposal is Bucket A only.** Buckets B/D need no action; Bucket C is deliberately
deferred rather than bundled in, since its dependents span both sides of the split.

## 3. What "re-home" concretely requires

1. **A new IES-owned `$id` namespace.** Current `$id`s are `https://schema.beckn.io/EnergyResource/v2.1`,
   `https://schema.beckn.io/ElectricityCredential/v1.2`, etc. Candidate patterns (governance to
   choose; **not decided here**):
   - `https://schema.iesaccelerator.in/EnergyResource/v2.1` (mirrors the existing path shape)
   - `https://schema.indiaenergystack.gov.in/...` (if IES has/will have a `.gov.in` presence)
   - Continue publishing under `schema.beckn.io/deg/...` but with IES as the named maintainer/CODEOWNER
     of just the Bucket-A paths (lowest-friction, no URL break, but doesn't fully resolve the
     "who edits this" ambiguity — worth floating as a middle option to DEG governance)
2. **Consumer continuity.** Anything that resolves `schema.beckn.io/EnergyResource/*` today
   (other DEG-ecosystem implementers, not just `ies-accelerator`) must keep working. Options:
   dual-publish at both URLs for a deprecation window with the old URL redirecting or serving an
   HTTP `Link` header to the new canonical, or a permanent alias. This needs DEG's sign-off,
   since it's their domain and their other consumers.
3. **Versioning carry-over.** The re-homed schemas keep their existing version numbers
   (`EnergyResource/v2.1`, `ElectricityCredential/v1.2`) at move time — this is a custody change,
   not a breaking schema revision. Citation corrections already on
   `fix/standards-conformance-citations` (commits `f03bd27`, `8056b92`) become the first IES-authored
   revision once the move lands.
4. **Tooling.** `attributes.yaml` files across the repo `$ref` the old URLs (see the full
   enumeration below); these need updating in the same change that flips the `$id`s. The
   `scripts/generate_*` build pipeline should be re-pointed to build from the IES-owned source
   instead of fetching/bundling from `schema.beckn.io`.
5. **Governance sign-off, both sides.** IES needs to accept ownership (maintenance burden, review
   process, standards-currency upkeep — exactly the job this review just did once). Beckn/DEG
   needs to agree to cede authorship of Bucket A while continuing to consume it via `$ref` for
   its own transaction schemas (Bucket B still needs `EnergyResource` to describe *what* is being
   traded, even though it no longer *owns* that description).

## 4. Full current upstream dependency graph (for reference)

All distinct `schema.beckn.io` references found in the repo today, for whoever scopes the actual
migration PR:

```
Address/v2.0, BecknTimeSeries/v1.0, ConsumptionProfileCredential/v2.0, CustomerDetails/v1.0,
DEGContract/v2.0, DemandFlexBuyOffer/v2.0, DemandFlexNeed/v2.0, DemandFlexPerformance/v2.0,
ElectricityCredential/{v1.0,v1.1,v1.2}, EnergyCredential/v2.0, EnergyCustomer/v2.0,
EnergyCustomerProfile/v1.0, EnergyOrderItem/v2.0, EnergyResource/{v2.0,v2.1},
EnergyTradeOffer/v2.0, GenerationProfileCredential/v2.0, GeoJSONGeometry/v2.0, IdRef/v1.0,
Location/2.0, MeterServiceProfile/v1.1, P2PTrade/v2.0, RevenueFlow/v2.0,
StorageProfileCredential/v2.0
```

## 5. Recommended next step

Take this document (Bucket A scope, the three `$id` options in §3.1, and the consumer-continuity
question in §3.2) to a joint IES/Beckn-DEG governance conversation. This branch's citation fixes
(`f03bd27`, `8056b92`) are a worked demonstration of exactly the content that would move — they
don't need to be redone if re-homing is approved; they'd simply be re-applied against the new
IES-owned source instead of the local mirror.

## 6. Explicitly out of scope for this proposal

- Any change to Bucket B (Beckn/DEG's transaction/marketplace schemas) — no re-homing case exists
  for these; they are correctly DEG's.
- Resolving Bucket C — deferred to a follow-up proposal once Bucket A's mechanics (namespace,
  consumer-continuity approach) are settled, since Bucket C's dependents span both buckets.
- Actually executing the move (new `$id`s, redirects, repo restructuring, updating every
  `attributes.yaml` `$ref`) — that's a follow-on implementation PR once governance approves the
  approach, not this document.
