# Behavioral-diversity evidence matrix

Synthetic decisions, not real audience forecasts. No quota required disagreement.

| Policy | Status | Anchors reproduced on heldout task |
|---|---|---|
| Time-limited beginner | not-yet-demonstrated | none |
| Evidence-demanding expert | not-yet-demonstrated | none |
| Privacy-constrained operator | retain-prototype | privacy |
| Convenience-focused operator | not-yet-demonstrated | none |
| Recovery-focused maintainer | not-yet-demonstrated | none |
| Exploratory maker | not-yet-demonstrated | none |

## Paired effects

Interest is ordinal (low / medium / high); vectors show repeated changes relative to the preregistered reference policy.

| Pair | Target / reference | Differential directions | Supported |
|---|---|---|---|
| development-proof | p02 / p01 | [0, 0] | False |
| development-language | p01 / p02 | [0, 0] | False |
| development-pace | p01 / p02 | [0, 0] | False |
| development-privacy | p03 / p04 | [1, 1] | True |
| development-friction | p04 / p03 | [2, -1] | False |
| development-recovery | p05 / p06 | [1, 0] | False |
| development-interaction | p06 / p05 | [0, 0] | False |
| heldout-proof | p02 / p01 | [0, 0, 0] | False |
| heldout-language | p01 / p02 | [1, 0, 0] | False |
| heldout-pace | p01 / p02 | [1, 1, 0] | True |
| heldout-privacy | p03 / p04 | [2, 2, 2] | True |
| heldout-friction | p04 / p03 | [0, 0, 1] | False |
| heldout-recovery | p05 / p06 | [1, 1, 1] | True |
| heldout-interaction | p06 / p05 | [0, 1, 0] | False |

## Supporting reactions

All paired repetitions are included below, including agreement and failures; not selected best cases.

### development-proof

- p01 repeat 1: medium → medium; low: No actual cleaned example shown, and trim wording is unclear for me.; high: Early fix helped, and this stays short and plain so I keep watching.. Evidence jobs: 5149f43267c8d282 / 3971a627e39b4911.
- p01 repeat 2: medium → medium; low: Simple one-click steps make cleaning sound easy and safe to try.; high: Plain steps confirm it stays effortless, worth staying for the result.. Evidence jobs: dbba5f3bf5f640d4 / 3e8da3d64837f762.
- p02 repeat 1: medium → medium; low: Concrete operation defined, need to see actual input-output demonstration.; high: Explains mechanism clearly but still no visible input-output comparison.. Evidence jobs: 5149f43267c8d282 / 3971a627e39b4911.
- p02 repeat 2: medium → medium; low: Operation defined precisely but no input-output to inspect yet, keep watching.; high: Explains Clean action, on-device processing, and undo; matches toy cleanup demo.. Evidence jobs: dbba5f3bf5f640d4 / 3e8da3d64837f762.

### development-language

- p01 repeat 1: medium → medium; low: Simple one-click cleanup with undo feels safe and easy, worth staying.; high: Clear one-click cleanup with undo feels safe and immediately useful.. Evidence jobs: f90117eaa6f96be5 / 7b43079581ad1a69.
- p01 repeat 2: medium → medium; low: One click to tidy spaces with undo feels safe and simple enough to use.; high: Clear one-click cleanup with undo feels safe and immediately useful.. Evidence jobs: d8e027ba9186d76f / bc72962e072f5c8f.
- p02 repeat 1: medium → medium; low: Mechanism now explicit and matches observed output; demo feels complete.; high: Trim and collapse definition answers what changed and why.. Evidence jobs: f90117eaa6f96be5 / 7b43079581ad1a69.
- p02 repeat 2: medium → medium; low: Operation precisely defined but no before-after input-output visible to verify claim.; high: Explanation matches observed cleanup; definition is precise and testable.. Evidence jobs: d8e027ba9186d76f / bc72962e072f5c8f.

### development-pace

- p01 repeat 1: medium → medium; low: Clear before-and-after shows immediate tidy-up value without learning anything hard.; high: One clear Clean button to tidy spaces feels quick and safe with undo.. Evidence jobs: 5b31df998e17617d / 1fe46427e235d9f1.
- p01 repeat 2: medium → medium; low: Now I see it tidies extra spaces, simple and immediately useful.; high: One click Clean with undo sounds safe and easy, keeps value clear.. Evidence jobs: a3612dacb7555b08 / 538804bffd06778e.
- p02 repeat 1: medium → medium; low: Input and output both visible so operation is inspectable.; high: Mechanism is specified clearly enough to judge credibility of toy workflow.. Evidence jobs: 5b31df998e17617d / 1fe46427e235d9f1.
- p02 repeat 2: medium → medium; low: Concrete input-output visible; operation matches definition, worth continued inspection.; high: Mechanism clarified and matches prior demo; clip ending, no more to inspect.. Evidence jobs: a3612dacb7555b08 / 538804bffd06778e.

### development-privacy

- p03 repeat 1: low → medium; low: Hosted processing means sensitive material leaves device, unacceptable for my workflow.; high: On-device processing resolves earlier data concern; workflow looks safe to try.. Evidence jobs: 6bb8a00ce0bf5584 / df93e921906e923d.
- p03 repeat 2: low → medium; low: Hosted processing discloses working material, violates my local-only requirement, so I stop.; high: Confirms on-device processing, matches local-only workflow requirement.. Evidence jobs: 0b07ece853cbe4ea / d637b06b8e5e1d5f.
- p04 repeat 1: medium → medium; low: Single action removes manual cleanup, fits non-sensitive routine work.; high: One-click Clean with undo meets low-effort need for routine notes.. Evidence jobs: 6bb8a00ce0bf5584 / df93e921906e923d.
- p04 repeat 2: medium → medium; low: One-click cleanup with undo fits routine non-sensitive notes, hosted is acceptable.; high: One-click cleanup fits fewer-actions goal, but payoff is tiny spacing fix with undo safety.. Evidence jobs: 0b07ece853cbe4ea / d637b06b8e5e1d5f.

### development-friction

- p03 repeat 1: high → medium; low: On-device processing confirmed, matches local-only need so willing to try.; high: On-device processing confirmed, so sensitive material stays local.. Evidence jobs: fe511b87db7b3272 / 63df96097052a932.
- p03 repeat 2: medium → high; low: On-device processing resolves data concern, so willing to try local clean.; high: On-device statement resolves data location worry for sensitive material.. Evidence jobs: 1bacc90a4323b662 / 0cf3c727ed8829bf.
- p04 repeat 1: low → medium; low: Three steps for tiny spacing fix adds work without useful payoff.; high: One-click cleanup with undo matches routine notes need; no extra work shown.. Evidence jobs: fe511b87db7b3272 / 63df96097052a932.
- p04 repeat 2: medium → medium; low: Simple cleanup with undo fits routine work; three steps seem acceptable.; high: One-click cleanup with undo matches low-effort routine goal.. Evidence jobs: 1bacc90a4323b662 / 0cf3c727ed8829bf.

### development-recovery

- p05 repeat 1: low → medium; low: No undo and replaces the original, so loss risk stops me.; high: Undo confirmed to restore original, matching reversibility need; no need to continue.. Evidence jobs: 0e2b39053f7e72cd / 9c760d5cf9e3aad2.
- p05 repeat 2: low → medium; low: No undo that replaces original violates need to preserve work.; high: Undo path is explicit, so reversibility concern is resolved.. Evidence jobs: 192aff7ffff5394b / 01fd3a550de4384d.
- p06 repeat 1: medium → medium; low: Clear single action with honest no-undo limit; trivial but tryable on samples.; high: Operation is clear and tryable but remains trivial spacing cleanup only.. Evidence jobs: 0e2b39053f7e72cd / 9c760d5cf9e3aad2.
- p06 repeat 2: low → medium; low: Operation is clear and tryable but too trivial and familiar to open new possibilities.; high: Operation is understandable and tryable, though basic cleanup only.. Evidence jobs: 192aff7ffff5394b / 01fd3a550de4384d.

### development-interaction

- p05 repeat 1: medium → medium; low: Undo restoring original removes overwrite risk, fits reversible workflow need.; high: Undo restores original confirms reversible workflow I require to continue.. Evidence jobs: 068072af62762dbe / 23903ddb86b6376e.
- p05 repeat 2: medium → medium; low: Undo restores original confirms reversible workflow I wanted.; high: Undo and on-device predictable clean matches need to preserve originals without risk.. Evidence jobs: bd06b0623e9e8911 / 59c1c92d781a4212.
- p06 repeat 1: medium → medium; low: Operation is understandable and tryable with undo; want to see result possibilities.; high: Voice interaction now clear and tryable with undo safety, fits disposable experiment goal.. Evidence jobs: 068072af62762dbe / 23903ddb86b6376e.
- p06 repeat 2: medium → medium; low: Operation now understandable as single Clean click with undo, tryable on samples.; high: Voice command interaction now clear and tryable on sample, satisfies curiosity.. Evidence jobs: bd06b0623e9e8911 / 59c1c92d781a4212.

### heldout-proof

- p01 repeat 1: medium → medium; low: Simple action is clear but no visible result shown yet.; high: One clear action with undo makes value obvious without extra learning.. Evidence jobs: 847122a080c25c01 / 4f4a0a8d1c483381.
- p01 repeat 2: medium → medium; low: One click Clean with undo sounds quick and safe to try.; high: One clear button to tidy list feels easy, worth seeing result.. Evidence jobs: c2c96a9f1476b90f / b0671da5b5a9f409.
- p01 repeat 3: medium → medium; low: Plain steps and undo make it feel low-effort and understandable.; high: Clear simple one-click payoff with safety net; got what I needed.. Evidence jobs: 17bc2b1b25f683b8 / 9b0be8e2f4b6f3d5.
- p02 repeat 1: medium → medium; low: Rule is clear but no input-output to verify yet, waiting for demonstration.; high: Defines keep-first rule clearly; want to inspect actual input-output change.. Evidence jobs: 847122a080c25c01 / 4f4a0a8d1c483381.
- p02 repeat 2: medium → medium; low: Operation defined clearly but no before-after data to inspect yet.; high: Rule is now explicit and testable; want to see edge cases next.. Evidence jobs: c2c96a9f1476b90f / b0671da5b5a9f409.
- p02 repeat 3: medium → medium; low: Rule is now precise but I have not seen what changed.; high: Rule is explicit and inspectable, satisfying credibility check for this toy workflow.. Evidence jobs: 17bc2b1b25f683b8 / 9b0be8e2f4b6f3d5.

### heldout-language

- p01 repeat 1: low → medium; low: Jargon title hard to understand, result not clearly useful yet; high: Steps look plain and short, payoff already clear so no need to continue.. Evidence jobs: 1b81b969abe142a5 / c355c63ca521da24.
- p01 repeat 2: medium → medium; low: Simple one-click cleanup with undo feels safe and worth trying.; high: One clear action with undo makes it feel safe and worth trying.. Evidence jobs: c4ecac3ff558bdab / bd8cb2f0658b9b99.
- p01 repeat 3: medium → medium; low: One simple Clean action with undo feels safe and easy to try.; high: Clear one-tap clean with undo feels safe and simple enough to try.. Evidence jobs: b3d6dae7f7def939 / 40e902ee088caec8.
- p02 repeat 1: medium → medium; low: Operation defined as keep-first dedup with local processing and undo; matches prior testable demo.; high: Rule and recovery are stated clearly; no new output to inspect in this card.. Evidence jobs: 1b81b969abe142a5 / c355c63ca521da24.
- p02 repeat 2: medium → medium; low: Operation defined precisely, matches prior dedup demo.; high: Mechanism explained clearly; no new output to inspect in this segment.. Evidence jobs: c4ecac3ff558bdab / bd8cb2f0658b9b99.
- p02 repeat 3: medium → medium; low: Mechanism precisely specified and matches prior stable dedup demonstration.; high: Rule is now explicit, but no new input-output change shown to verify.. Evidence jobs: b3d6dae7f7def939 / 40e902ee088caec8.

### heldout-pace

- p01 repeat 1: medium → high; low: Example now makes rows idea clear and quick to grasp.; high: Simple one-click cleanup with undo feels low effort and immediately useful.. Evidence jobs: c1800818bc755202 / 3dfdba05c5737a7b.
- p01 repeat 2: low → medium; low: Sounds technical about rows, no clear benefit shown yet, not worth attention.; high: Simple one-click cleanup with undo feels safe and clear.. Evidence jobs: 10be403e16a2d44a / ccc321a29210886f.
- p01 repeat 3: medium → medium; low: Now I see messy list becomes clean list without extra work.; high: Clear one-click cleanup with undo feels safe and quick to try.. Evidence jobs: 28b2de116f955fb7 / 85832d92a728ac2c.
- p02 repeat 1: medium → medium; low: Input-output shown with order preserved; credible demonstration worth finishing.; high: Operation rule stated clearly; demo ended so no further inspection possible.. Evidence jobs: c1800818bc755202 / 3dfdba05c5737a7b.
- p02 repeat 2: medium → medium; low: Concrete input-output visible; claim matches observable result for this case.; high: Operation now defined concretely; sufficient to judge toy workflow credible.. Evidence jobs: 10be403e16a2d44a / ccc321a29210886f.
- p02 repeat 3: medium → medium; low: Concrete before-after shows deduped order preserved, satisfying inspectability need.; high: Details match prior dedup demo and clarify operation.. Evidence jobs: 28b2de116f955fb7 / 85832d92a728ac2c.

### heldout-privacy

- p03 repeat 1: low → high; low: Hosted service means sensitive material leaves device, so I stop.; high: On-device processing resolves data-handling worry, workflow looks controllable.. Evidence jobs: 58b0d173204d2310 / 6355e32c87e16160.
- p03 repeat 2: low → high; low: Hosted processing sends material externally with no local option, violates control requirement.; high: On-device processing resolves data-location worry; Clean with undo looks safe.. Evidence jobs: e7c134acc9e1006e / 035fc381b0a833f1.
- p03 repeat 3: low → high; low: Hosted processing sends material externally with no local alternative shown.; high: On-device processing resolves earlier data-location caution.. Evidence jobs: f81cca53bc341926 / 0bf721dbe6b7797a.
- p04 repeat 1: high → high; low: One-click clean with undo and disclosed hosted processing fits routine non-sensitive lists perfectly.; high: One action to clean with undo matches my low-effort goal.. Evidence jobs: 58b0d173204d2310 / 6355e32c87e16160.
- p04 repeat 2: high → high; low: One-click Clean with undo fits goal of fewer actions for routine cleanup.; high: One-click dedup with undo and on-device processing fits my routine cleanup goal perfectly.. Evidence jobs: e7c134acc9e1006e / 035fc381b0a833f1.
- p04 repeat 3: high → high; low: One action with undo confirms real time saving without added work.; high: Single Clean action promises fewer manual steps with safety net.. Evidence jobs: f81cca53bc341926 / 0bf721dbe6b7797a.

### heldout-friction

- p03 repeat 1: medium → medium; low: On-device processing resolves data-location worry; workflow looks controllable and safe to try.; high: On-device processing resolves data disclosure worry for this workflow.. Evidence jobs: 9374231521629875 / 8ebc1febd07ac0fb.
- p03 repeat 2: medium → medium; low: On-device processing resolves data-location worry, so workflow looks acceptable to try.; high: On-device processing resolves earlier concern, so this local workflow looks safe to try.. Evidence jobs: a5d763fa6406bc53 / 37916a667142e0e0.
- p03 repeat 3: medium → medium; low: On-device processing resolves data-location worry; simple reversible steps fit local workflow.; high: On-device statement resolves data-location worry for sensitive material.. Evidence jobs: e72b878f6de0dcff / 3dddaada3ebdc93a.
- p04 repeat 1: high → high; low: Three simple steps with undo fit routine cleanup and save manual work.; high: One-click Clean with undo matches low-effort cleanup goal perfectly.. Evidence jobs: 9374231521629875 / 8ebc1febd07ac0fb.
- p04 repeat 2: high → high; low: Three steps and undo look low-effort for my dedup cleanup.; high: One-click cleanup with undo directly cuts manual dedupe work, matching goal.. Evidence jobs: a5d763fa6406bc53 / 37916a667142e0e0.
- p04 repeat 3: medium → high; low: Three manual steps feels like extra work for simple dedupe task.; high: Single Clean action promises fewer steps with safe undo.. Evidence jobs: e72b878f6de0dcff / 3dddaada3ebdc93a.

### heldout-recovery

- p05 repeat 1: low → medium; low: No undo that replaces original violates reversibility requirement; cannot risk existing work.; high: Undo restores original answers my reversibility worry for workflow.. Evidence jobs: 578ed63a548a023f / 37e5db3205f43784.
- p05 repeat 2: low → medium; low: No undo that replaces original violates need to preserve work.; high: Undo restores original and single Clean action makes workflow predictable and reversible.. Evidence jobs: 89c38272d23bec8b / 523ca822a45be292.
- p05 repeat 3: low → medium; low: No undo replacing original violates preserve-and-recover requirement.; high: Undo restores original satisfies recovery need; predictable one-action workflow.. Evidence jobs: 704bb694161466d9 / 408badf9c6ccc4c0.
- p06 repeat 1: medium → medium; low: Operation now understandable: one Click Clean keeps first row.; high: Operation now understandable and tryable, matches curiosity to test it.. Evidence jobs: 578ed63a548a023f / 37e5db3205f43784.
- p06 repeat 2: medium → medium; low: One clear Clean action to try on samples despite no undo.; high: Explains exactly how to trigger Clean, satisfying prior curiosity.. Evidence jobs: 89c38272d23bec8b / 523ca822a45be292.
- p06 repeat 3: medium → medium; low: Clear single-click dedup with honest no-undo limit makes operation understandable and tryable on samples.; high: Clear interaction finally shown with undo, understandable enough to try on samples.. Evidence jobs: 704bb694161466d9 / 408badf9c6ccc4c0.

### heldout-interaction

- p05 repeat 1: medium → medium; low: Undo now explicitly restores original, resolving my main worry about overwriting work.; high: Undo restores original resolves prior safety concern about overwriting work.. Evidence jobs: f1898544e71e8688 / 84df7ca01cc825a5.
- p05 repeat 2: medium → medium; low: Undo now explicit, single predictable action preserves first rows.; high: Undo restores original resolves my recovery worry; operation looks predictable now.. Evidence jobs: 4e4b5ec725fe8a00 / f25ab64cba2fd673.
- p05 repeat 3: medium → medium; low: Undo guarantee answers preservation worry; workflow looks predictable and safe.; high: Undo restores original resolves preservation worry; predictable workflow.. Evidence jobs: 3463455c2a243dac / 69d3546483f37a0b.
- p06 repeat 1: medium → medium; low: Interaction is now understandable and tryable on disposable sample, matches curiosity.; high: Clear voice action and undo make it understandable and worth trying on samples.. Evidence jobs: f1898544e71e8688 / 84df7ca01cc825a5.
- p06 repeat 2: medium → high; low: Got how to trigger Clean and undo safety; ready to try on sample.; high: Concrete trigger plus undo makes the interaction understandable and tryable. Evidence jobs: 4e4b5ec725fe8a00 / f25ab64cba2fd673.
- p06 repeat 3: medium → medium; low: Operation now understandable and triable on samples; want to see result.; high: Voice action and undo make operation understandable and tryable on samples.. Evidence jobs: 3463455c2a243dac / 69d3546483f37a0b.
