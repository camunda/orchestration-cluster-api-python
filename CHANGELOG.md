# CHANGELOG

<!-- version list -->

## v8.9.0-dev.35 (2026-04-12)

### Bug Fixes

- Address PR #92 review comments
  ([`6b59d7c`](https://github.com/camunda/orchestration-cluster-api-python/commit/6b59d7ccd40a1dfe3c48d46317aef1ee941eb3e1))

- Remove all type: ignore comments from integration tests
  ([`5ae5017`](https://github.com/camunda/orchestration-cluster-api-python/commit/5ae501755c46fd672fd56fde300ba77796e95b97))

- Replace invalid AdvancedStringFilter(gte=) with like= in variables test
  ([`79cd1d3`](https://github.com/camunda/orchestration-cluster-api-python/commit/79cd1d3bce1269423c7d385364ec60308af0f534))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`245b587`](https://github.com/camunda/orchestration-cluster-api-python/commit/245b5873a7c939a115e16dbdd6fa4b4e30ccc935))

### Testing

- Integration test suite for search_process_instances filter and pagination shapes
  ([`0f9807a`](https://github.com/camunda/orchestration-cluster-api-python/commit/0f9807a17369692d206ca4117987cc7d2513bf91))


## v8.9.0-dev.34 (2026-04-12)

### Bug Fixes

- Remove unnecessary f-string prefix
  ([`671108e`](https://github.com/camunda/orchestration-cluster-api-python/commit/671108e0536e142ba42ca0b0f460aeb463dd400d))

### Chores

- Address review comments
  ([`9baab86`](https://github.com/camunda/orchestration-cluster-api-python/commit/9baab86dd7dcdbe6acc4ccd82afa5ea9ea70fee1))

- **generation**: Update generated SDK [skip ci]
  ([`ae0445e`](https://github.com/camunda/orchestration-cluster-api-python/commit/ae0445e2f2489252ce9e710c271023a2fe84e5fb))

- **generation**: Update generated SDK [skip ci]
  ([`a7705df`](https://github.com/camunda/orchestration-cluster-api-python/commit/a7705df3a222e31ce6d845f2a1a3edc5bf6170a2))

- **generation**: Update generated SDK [skip ci]
  ([`17f1acb`](https://github.com/camunda/orchestration-cluster-api-python/commit/17f1acb8966fca0730fdcefdf1d87ce103fc2482))

### Documentation

- Add 'prefer ergonomic helpers' guideline to copilot-instructions
  ([`a1f4e6b`](https://github.com/camunda/orchestration-cluster-api-python/commit/a1f4e6b4ce22399cb9f63bacf365f562a13e7749))

- Update semantic types section to reflect class-based implementation
  ([`5e4e05f`](https://github.com/camunda/orchestration-cluster-api-python/commit/5e4e05f749835e814c2d0666876c3b71ff639ccb))

### Refactoring

- Make semantic types class-based with built-in validation
  ([`3f0844f`](https://github.com/camunda/orchestration-cluster-api-python/commit/3f0844fb116407dfa2ad744c1bafb07df387d384))

- Remove lift_* helpers — class constructors are the single API surface
  ([`d41ead0`](https://github.com/camunda/orchestration-cluster-api-python/commit/d41ead07b3456cca5de7029fe17ca5a63a413efb))

### Testing

- Add semantic types behavioral regression guard
  ([`c4dbe22`](https://github.com/camunda/orchestration-cluster-api-python/commit/c4dbe225d530412cb23202d62eb5d32b48031988))


## v8.9.0-dev.33 (2026-04-09)

### Bug Fixes

- Add missing example regions for hand-written client methods
  ([`3f010a3`](https://github.com/camunda/orchestration-cluster-api-python/commit/3f010a370a44aa6c57a42fd0053311303276a898))

- Validate operation-map file+region references exist
  ([`bc86c4d`](https://github.com/camunda/orchestration-cluster-api-python/commit/bc86c4d730ac07c6e049f3646f1c31093e694d59))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`e6d10b5`](https://github.com/camunda/orchestration-cluster-api-python/commit/e6d10b580697dcd5c210a962642ed0aa841f9fee))

### Testing

- Add CI guard for method example completeness
  ([`71c5f54`](https://github.com/camunda/orchestration-cluster-api-python/commit/71c5f54f39626641e7555ba0cc93b891a8dc59cf))


## v8.9.0-dev.32 (2026-04-08)

### Bug Fixes

- Add isinstance(entry, dict) check before accessing entry fields
  ([`47cda2c`](https://github.com/camunda/orchestration-cluster-api-python/commit/47cda2c23dedd9c083cbe376a11a85a273f58175))

- Broken links in docs synced to camunda-docs
  ([`efc1258`](https://github.com/camunda/orchestration-cluster-api-python/commit/efc12586d0521145a4daf0dfdb37c3cab70042aa))

- Shorten discriminant labels for multi-entry operations
  ([`88a8839`](https://github.com/camunda/orchestration-cluster-api-python/commit/88a88392991fbb01ba13b211948f4fb33099f410))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`a5a7ed9`](https://github.com/camunda/orchestration-cluster-api-python/commit/a5a7ed9561b3e866ca0f5b4b7ee3f930e1f724fe))

### Features

- Add imports field to operation-map entries
  ([`aeee349`](https://github.com/camunda/orchestration-cluster-api-python/commit/aeee349233b623c0a8f8be3d35962cd0deafe625))

### Refactoring

- Move imports to defaultImports in docusaurus config
  ([`9504c1a`](https://github.com/camunda/orchestration-cluster-api-python/commit/9504c1ac2f2b61ad419d4d66929ea6e037e46a8f))


## v8.9.0-dev.31 (2026-04-06)

### Bug Fixes

- Improve API reference formatting in generated docs
  ([`f344e13`](https://github.com/camunda/orchestration-cluster-api-python/commit/f344e137c3db2f4a94efbd7c1580911d535e52a4))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`10cc939`](https://github.com/camunda/orchestration-cluster-api-python/commit/10cc93982acd283364b4c3097360e76f11a13b0e))


## v8.9.0-dev.30 (2026-04-06)

### Bug Fixes

- Broken links in docs synced to camunda-docs
  ([`467ca24`](https://github.com/camunda/orchestration-cluster-api-python/commit/467ca24eb507d40bf3e672aca25ccb8f92c1e696))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`195f237`](https://github.com/camunda/orchestration-cluster-api-python/commit/195f2373ee2a5d74a15846a0dcd44a67ed03e6e3))

- **generation**: Update generated SDK [skip ci]
  ([`18e0c2a`](https://github.com/camunda/orchestration-cluster-api-python/commit/18e0c2ae4e3e0bf1c47b74ffb5a15cde5d9edba8))

- **generation**: Update generated SDK [skip ci]
  ([`5d810fa`](https://github.com/camunda/orchestration-cluster-api-python/commit/5d810fa1100201d96bbcebc48b0b082a511a53a8))

### Documentation

- Require red/green refactor discipline for all bug fixes
  ([`192e54c`](https://github.com/camunda/orchestration-cluster-api-python/commit/192e54cf3c3274eed56b65e0cc2a0dd5d1d468ed))

- Update snippet format and add README examples section to CONTRIBUTING
  ([`e3ec9fa`](https://github.com/camunda/orchestration-cluster-api-python/commit/e3ec9fac744a5ae657ab3fef10c986996e9b5579))


## v8.9.0-dev.29 (2026-04-02)

### Bug Fixes

- Consistent TLS for OAuth transport + secure temp file permissions
  ([`b9631c0`](https://github.com/camunda/orchestration-cluster-api-python/commit/b9631c0288399e621674141e1446baaf3ad4a59d))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`881a0d0`](https://github.com/camunda/orchestration-cluster-api-python/commit/881a0d0dd16f6aab87c9a57289c9933c04f42a1f))

### Features

- Support CA-only TLS (self-signed server certs)
  ([`a354bbb`](https://github.com/camunda/orchestration-cluster-api-python/commit/a354bbb7dc8d0611615056840b11fbd3370a6b5f))

- Support custom TLS certificates (mTLS)
  ([`36eb691`](https://github.com/camunda/orchestration-cluster-api-python/commit/36eb691826838d6f4ca921169308e7d1b47ed2cc))


## v8.9.0-dev.28 (2026-04-01)

### Bug Fixes

- Address PR review comments
  ([`d97ff72`](https://github.com/camunda/orchestration-cluster-api-python/commit/d97ff728ab815ef02715008cc026720e1f825562))

- Address review feedback on document/variable examples
  ([`9e2bcba`](https://github.com/camunda/orchestration-cluster-api-python/commit/9e2bcba14e55a7c9065ce9463f5a0a45f4cd8027))

- Pass decision_definition_key in get_decision_definition example
  ([`fb58542`](https://github.com/camunda/orchestration-cluster-api-python/commit/fb58542f1f8c4e9b689d69816ce1fbe0b61fc8c1))

- Remove get_status example (method not yet on CamundaClient)
  ([`a2b6f35`](https://github.com/camunda/orchestration-cluster-api-python/commit/a2b6f35ca2e6ab751d1cb8082dd8b7f4e647d1d9))

- Remove unused ProcessDefinitionKey import
  ([`c7ac5c5`](https://github.com/camunda/orchestration-cluster-api-python/commit/c7ac5c55ef5a1c7ab0cbafbfc0ee20d003f8e1de))

- Restore get_status example (method now available after PR #69 merge)
  ([`a258701`](https://github.com/camunda/orchestration-cluster-api-python/commit/a2587016e65bb0f6e0844043beed7d80af9fa83d))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`b1c16ee`](https://github.com/camunda/orchestration-cluster-api-python/commit/b1c16eed4f54c97891ae7051b366534d4b69ea6e))

### Documentation

- Add Copilot prompt files
  ([`9d81076`](https://github.com/camunda/orchestration-cluster-api-python/commit/9d810764f219353fb872fe5c0137c8a33d1b8fe2))

- Add examples for document and effective variable operations
  ([`1a00a88`](https://github.com/camunda/orchestration-cluster-api-python/commit/1a00a885ae1072825ff532f4f44416bbc08e7615))

- Parameterize SDK examples and add coverage tooling
  ([`7f541ea`](https://github.com/camunda/orchestration-cluster-api-python/commit/7f541eae22da4431650f7d7508be684bd5789916))

- Sync README snippets
  ([`3b43d65`](https://github.com/camunda/orchestration-cluster-api-python/commit/3b43d6555cf7c9cfdbf9fc2ccf461e6b63bcc8b7))


## v8.9.0-dev.27 (2026-04-01)

### Build System

- **deps**: Bump actions/checkout from 4 to 6
  ([`9c8ac02`](https://github.com/camunda/orchestration-cluster-api-python/commit/9c8ac02dc5798fadebf9f211ea933ce29c388a42))

- **deps**: Bump actions/configure-pages from 5 to 6
  ([`51d40fb`](https://github.com/camunda/orchestration-cluster-api-python/commit/51d40fb86df229af65c098a8ea65b7ed55d3d2d5))

- **deps**: Bump actions/deploy-pages from 4 to 5
  ([`a83ea27`](https://github.com/camunda/orchestration-cluster-api-python/commit/a83ea2765d46ae6d0b537baddfed062226d3ba5e))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`d6ddf40`](https://github.com/camunda/orchestration-cluster-api-python/commit/d6ddf40e4bfbe64a845f166afd6356dcc0f952d1))

### Features

- Embed specHash from spec-metadata.json in published package
  ([`d14e039`](https://github.com/camunda/orchestration-cluster-api-python/commit/d14e039d96e600e546d67cad5e50d2711388c635))

### Refactoring

- Harden spec hash emission per review feedback
  ([`27381c7`](https://github.com/camunda/orchestration-cluster-api-python/commit/27381c7ae1ef98abeff52f31e01232fa8c20e07d))


## v8.9.0-dev.26 (2026-03-31)

### Bug Fixes

- Inject default tenant ID into request body, not path params
  ([`97d8145`](https://github.com/camunda/orchestration-cluster-api-python/commit/97d8145c5c72ecf075cc3d4be441e4de730cf863))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`1b0c57c`](https://github.com/camunda/orchestration-cluster-api-python/commit/1b0c57c7c7a8e1118899202737271d6612059bf2))


## v8.9.0-dev.25 (2026-03-31)

### Bug Fixes

- Address PR review comments on synthesized convenience wrappers
  ([`6198953`](https://github.com/camunda/orchestration-cluster-api-python/commit/61989539013ac246e57772f8e0dbf8e4a1611d6d))

- Expose body-less endpoints (e.g. getStatus) on CamundaClient
  ([`50d6b8e`](https://github.com/camunda/orchestration-cluster-api-python/commit/50d6b8e39932beff6282b42dc516d35fe4c10366))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`abdb8e0`](https://github.com/camunda/orchestration-cluster-api-python/commit/abdb8e06b1fd87d5a7e68f2d725619570706fd64))


## v8.9.0-dev.24 (2026-03-31)

### Bug Fixes

- Harden README code injection
  ([`7dcf7e3`](https://github.com/camunda/orchestration-cluster-api-python/commit/7dcf7e304385138e4c5406774d5074fcc11f9172))

### Build System

- **deps**: Bump actions/setup-node from 4 to 6
  ([`bd62991`](https://github.com/camunda/orchestration-cluster-api-python/commit/bd629915e1a95e48b9788d8484e787bf2c3cbb49))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`21a182d`](https://github.com/camunda/orchestration-cluster-api-python/commit/21a182d4096941fdf3ebb38623945338a22b3124))

- **generation**: Update generated SDK [skip ci]
  ([`8a934c7`](https://github.com/camunda/orchestration-cluster-api-python/commit/8a934c73e40e27b1d205d2e503732998f646b288))

### Documentation

- Fix examples
  ([`27cd67e`](https://github.com/camunda/orchestration-cluster-api-python/commit/27cd67e50caa5453a32daea15456e5df5baf9b30))


## v8.9.0-dev.23 (2026-03-27)

### Build System

- **deps**: Bump actions/configure-pages from 4 to 5
  ([`ef7a38c`](https://github.com/camunda/orchestration-cluster-api-python/commit/ef7a38c5de824aca783f98e567b87fc91835276e))

- **deps**: Bump actions/setup-python from 5 to 6
  ([`180b10b`](https://github.com/camunda/orchestration-cluster-api-python/commit/180b10b06bd0d1b07109f3a3a5f9bab52aa295e3))

- **deps**: Bump actions/upload-pages-artifact from 3 to 4
  ([`9d2ec81`](https://github.com/camunda/orchestration-cluster-api-python/commit/9d2ec812ee2d7830ffccb45ecff54c52b230c4a2))

- **deps**: Bump astral-sh/setup-uv from 5 to 7
  ([`92b3bb4`](https://github.com/camunda/orchestration-cluster-api-python/commit/92b3bb457b16c3d5d667e1d638d1fc3cb1d13051))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`b614759`](https://github.com/camunda/orchestration-cluster-api-python/commit/b6147593dd36ba00515a99991f7cc02642ae97e4))

- **generation**: Update generated SDK [skip ci]
  ([`2b45994`](https://github.com/camunda/orchestration-cluster-api-python/commit/2b45994164f029bdac003c63794005e5efda7d31))

### Features

- Heritable worker configuration defaults
  ([`2bcccc2`](https://github.com/camunda/orchestration-cluster-api-python/commit/2bcccc23a6623fdef7b1580eef9120197e7bf394))


## v8.9.0-dev.22 (2026-03-27)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`1e67a29`](https://github.com/camunda/orchestration-cluster-api-python/commit/1e67a29a563b086f78aa8ee1619b6ed9e0463ae0))

### Features

- Support job corrections in worker framework
  ([`295a9c3`](https://github.com/camunda/orchestration-cluster-api-python/commit/295a9c3c2dacf474d9d41b26d416a44885141954))


## v8.9.0-dev.21 (2026-03-27)

### Chores

- Regenerate SDK with transcendent tenant_id support
  ([`bfc8034`](https://github.com/camunda/orchestration-cluster-api-python/commit/bfc80343a9637cc3c0f86c0a260fdfc3a7e6d837))

- Remove black/pre-commit, split dep groups, fix method ordering
  ([`e1ae2b6`](https://github.com/camunda/orchestration-cluster-api-python/commit/e1ae2b62329df67357c2299d37516bed32a78b11))

- **generation**: Regenerate SDK with deterministic method ordering
  ([`4cf18a1`](https://github.com/camunda/orchestration-cluster-api-python/commit/4cf18a1812c6c7106ba90e0c2f4922b3179d28ad))

- **generation**: Update generated SDK [skip ci]
  ([`963d4de`](https://github.com/camunda/orchestration-cluster-api-python/commit/963d4de7a77d64b81854757ae700e8f768c08a9e))

- **generation**: Update generated SDK [skip ci]
  ([`8c96417`](https://github.com/camunda/orchestration-cluster-api-python/commit/8c96417bf9f089411939d2f00809f88b74a00b5c))

### Features

- Transcendent tenant_id configuration
  ([`1e80421`](https://github.com/camunda/orchestration-cluster-api-python/commit/1e8042168ce234ae824c5e18c23492d375010a3d))


## v8.9.0-dev.20 (2026-03-25)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`9d2979f`](https://github.com/camunda/orchestration-cluster-api-python/commit/9d2979f703182720f0509869f3bdeb6df26c5bfb))

### Continuous Integration

- Add Dependabot
  ([`07f1008`](https://github.com/camunda/orchestration-cluster-api-python/commit/07f1008b07cc7745aa1f3481d1456ee80a46af51))

### Features

- Replace per-operation exception classes with per-status exceptions
  ([`0665ce7`](https://github.com/camunda/orchestration-cluster-api-python/commit/0665ce7fb80fffd7de5fb356c8f5de817a61936f))


## v8.9.0-dev.19 (2026-03-25)

### Bug Fixes

- Correct GetStatus region and operation-map entries
  ([`d874823`](https://github.com/camunda/orchestration-cluster-api-python/commit/d8748237dbc2dead1660feeaed6bf30a23fb743e))

- Preserve isinstance guard for nullable semantic type fields
  ([`9e7d1dd`](https://github.com/camunda/orchestration-cluster-api-python/commit/9e7d1dd1ef9adaf94a666564b4428d0810d512aa))

### Build System

- Rebuild from upstream stable/8.9 spec, fix ScopeKey union type generation
  ([`e7f7e5f`](https://github.com/camunda/orchestration-cluster-api-python/commit/e7f7e5fad5d523443f44e91e51e3c6521439a3d6))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`d19eb7e`](https://github.com/camunda/orchestration-cluster-api-python/commit/d19eb7e4b03b3728aae8e760fc5f880276c765af))

- **generation**: Update generated SDK [skip ci]
  ([`09fa9f0`](https://github.com/camunda/orchestration-cluster-api-python/commit/09fa9f03b367b520cdde93db6f5656c1d46cb3e1))

### Documentation

- Add warning for maintainers to README
  ([`2e29088`](https://github.com/camunda/orchestration-cluster-api-python/commit/2e29088e12c1dad7a1fbbb12ef65138cb6d2f245))

- Expand SDK code examples to cover all API operations
  ([`d16a8ed`](https://github.com/camunda/orchestration-cluster-api-python/commit/d16a8edcd45779c424f5b669f527a7372cab476f))

- Update versioning scheme notes
  ([`93cc504`](https://github.com/camunda/orchestration-cluster-api-python/commit/93cc5047065fb97de2d436aae79791dc4763814e))


## v8.9.0-dev.18 (2026-03-23)

### Bug Fixes

- **generator**: Normalize bare $ref responses and fail on warnings
  ([`041f628`](https://github.com/camunda/orchestration-cluster-api-python/commit/041f628d95fc3e3e6495cae8f03e74080576461c))

### Chores

- **build**: Add example typecheck, README sync, and config reference to generate targets
  ([`1f98e92`](https://github.com/camunda/orchestration-cluster-api-python/commit/1f98e92776db919b7725271bfec01fe5603d0d62))

- **generation**: Update generated SDK [skip ci]
  ([`feece5d`](https://github.com/camunda/orchestration-cluster-api-python/commit/feece5dccfc373d798f68d590b171313a128d877))

### Documentation

- Document README examples integration
  ([`89e5d28`](https://github.com/camunda/orchestration-cluster-api-python/commit/89e5d288dfef0a74238453427b6abf7337c90c9e))

- Update section numbering
  ([`1686a3b`](https://github.com/camunda/orchestration-cluster-api-python/commit/1686a3bcd855f6df4d1d2dd27215e1a3065cafc1))


## v8.9.0-dev.17 (2026-03-23)

### Bug Fixes

- Rename ambiguous variable l to line (ruff E741)
  ([`3479c72`](https://github.com/camunda/orchestration-cluster-api-python/commit/3479c721458f8dd96515a9a15c9a230f97d9aea5))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`bca7a55`](https://github.com/camunda/orchestration-cluster-api-python/commit/bca7a55e1bb889e6e7dcbff2f532295fdc53d713))

### Documentation

- Add compilable README examples with snippet sync
  ([`fc33531`](https://github.com/camunda/orchestration-cluster-api-python/commit/fc335316c5dfdcc2f9391b7a271e1308b2b99900))


## v8.9.0-dev.16 (2026-03-20)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`870beda`](https://github.com/camunda/orchestration-cluster-api-python/commit/870beda220dda8c31e5879b6a21ac2d3cce442ee))

### Features

- Provide sync client to thread strategy handlers via SyncJobContext
  ([`5df28dd`](https://github.com/camunda/orchestration-cluster-api-python/commit/5df28dd04e529fd1735980368b02d7209505d99d))


## v8.9.0-dev.15 (2026-03-20)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`ae01c85`](https://github.com/camunda/orchestration-cluster-api-python/commit/ae01c859c0e11e938f2cd39b97165d3fcdcb4729))

### Features

- Enable single import point
  ([`74711b5`](https://github.com/camunda/orchestration-cluster-api-python/commit/74711b51a3332f450a1a08c4cb346412bd8a70c2))


## v8.9.0-dev.14 (2026-03-17)

### Bug Fixes

- Add note on execution strategy selection
  ([`5b28380`](https://github.com/camunda/orchestration-cluster-api-python/commit/5b28380de79043636f62cfc69cf8b483b991ff88))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`52e0e9f`](https://github.com/camunda/orchestration-cluster-api-python/commit/52e0e9f45626dbc82285722d47bb3e852a5da8fb))

### Documentation

- Add example of using ConnectedJobContext.client
  ([`58a5a20`](https://github.com/camunda/orchestration-cluster-api-python/commit/58a5a20755dc0e5e5440fb98bd64372fddc2e4d9))

- Add notes on failing jobs in worker
  ([`c76b21b`](https://github.com/camunda/orchestration-cluster-api-python/commit/c76b21b5cb8f4bf78bee030a979a10dfcfcf7264))

### Features

- Build from latest stable/8.9
  ([`1010df7`](https://github.com/camunda/orchestration-cluster-api-python/commit/1010df7856eb72e38f76c739b38a28ce06ebe169))


## v8.9.0-dev.13 (2026-03-09)

### Bug Fixes

- Don't send tenant_filter on job activation if not provided by user
  ([`96d1039`](https://github.com/camunda/orchestration-cluster-api-python/commit/96d103935b5129c6e4868b4d08cf66b8832e0504))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`f90ad47`](https://github.com/camunda/orchestration-cluster-api-python/commit/f90ad47b1e8efd959464a9608f09f92b74793d80))


## v8.9.0-dev.12 (2026-03-09)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`289d4b6`](https://github.com/camunda/orchestration-cluster-api-python/commit/289d4b6b259d143421a4ddd881cfe43a987b59a0))

### Features

- Tolerate missing in nullable field (supports 8.8 behaviour) for deploy_resources_from_files
  ([`ae5147a`](https://github.com/camunda/orchestration-cluster-api-python/commit/ae5147ac2fd97fa123b9b4b7af1ffe8d83169496))


## v8.9.0-dev.11 (2026-03-09)

### Bug Fixes

- Update configuration reference, add note to backpressure docs with stats
  ([`42b4087`](https://github.com/camunda/orchestration-cluster-api-python/commit/42b4087f184b36e3cf950b0492799180fe8abf34))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`4ebe6ff`](https://github.com/camunda/orchestration-cluster-api-python/commit/4ebe6ffec4eb2b7da0d901517bab5fd9aa39b0fd))

### Features

- Add backpressure implementation and scenario test matrix
  ([`528df22`](https://github.com/camunda/orchestration-cluster-api-python/commit/528df223bf94dcf7721affc755f18cd40da14848))


## v8.9.0-dev.10 (2026-03-05)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`2ca59bf`](https://github.com/camunda/orchestration-cluster-api-python/commit/2ca59bf32e9a1350550afde2bb043d75e1b19dd7))

### Features

- Add startup jitter to job worker
  ([`e4dbe99`](https://github.com/camunda/orchestration-cluster-api-python/commit/e4dbe99f2e4f5e193e40cc0a31fbef4ed4b8efb6))


## v8.9.0-dev.9 (2026-03-04)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`cc8c794`](https://github.com/camunda/orchestration-cluster-api-python/commit/cc8c794e39a615a2cc2c4298ec3fce9f28f06e0f))

### Features

- Add client to JobContext for async and thread execution strategy
  ([`d30e519`](https://github.com/camunda/orchestration-cluster-api-python/commit/d30e51931034cbb13cc30db0a5ded6f8cbe99dfc))


## v8.9.0-dev.8 (2026-03-03)

### Bug Fixes

- Correctly handle nullable fields
  ([`a6464ce`](https://github.com/camunda/orchestration-cluster-api-python/commit/a6464ceba75889e53d32c98fd0debeab8e0c88d6))

- Correctly validate .env file
  ([`a03d5b9`](https://github.com/camunda/orchestration-cluster-api-python/commit/a03d5b933a0da98cb6318ed02f4c3a5a5265c5b8))

- Rebuild with latest spec
  ([`9212968`](https://github.com/camunda/orchestration-cluster-api-python/commit/9212968c9f996321cb0c3dd555db8c142a4a2e66))

- Regenerate from main
  ([`ea00363`](https://github.com/camunda/orchestration-cluster-api-python/commit/ea0036359a49c3826fe5fcc20885c2c534ee33b0))

### Chores

- Remove tmp clone files
  ([`946be52`](https://github.com/camunda/orchestration-cluster-api-python/commit/946be52e31212aed7999e46280a8c43800bca823))

- **generation**: Update generated SDK [skip ci]
  ([`eff7dba`](https://github.com/camunda/orchestration-cluster-api-python/commit/eff7dbad45e4d8da38e2ef5ede4b490007bd536a))

### Continuous Integration

- Update Camunda Docs integration
  ([`8f3675a`](https://github.com/camunda/orchestration-cluster-api-python/commit/8f3675aa004ff44053d309e7c2577b2f7b7cd493))

- Use 8.9-SNAPSHOT for integration test
  ([`89307e3`](https://github.com/camunda/orchestration-cluster-api-python/commit/89307e335cbff359b8b18333c0519ae9544346df))

### Features

- Support deprecated enum members
  ([`b1448ec`](https://github.com/camunda/orchestration-cluster-api-python/commit/b1448ecb38435467ea1c632214b827ed6771dae8))


## v8.9.0-dev.7 (2026-02-17)

### Bug Fixes

- Use camunda-schema-bundler 1.3.3. **breaking type changes**
  ([`bc8d777`](https://github.com/camunda/orchestration-cluster-api-python/commit/bc8d7774cb2eba13653371a001cba478d64aceb7))

### Chores

- Add linting and typecheck precommit hook
  ([`e3bcc05`](https://github.com/camunda/orchestration-cluster-api-python/commit/e3bcc05d16e02061db7b43aeedb9e927ea4fdda8))

- Update MAINTAINER doc with Docusarus integration
  ([`f7ccdcc`](https://github.com/camunda/orchestration-cluster-api-python/commit/f7ccdccc22b8fd2e1f19674f3482de32d2aa44cc))

- Use same code formatter in generation and precommit
  ([`d60f52b`](https://github.com/camunda/orchestration-cluster-api-python/commit/d60f52bf56ec0af32e1d263f4cb84841918e6e35))

- **generation**: Update generated SDK [skip ci]
  ([`9f3a43e`](https://github.com/camunda/orchestration-cluster-api-python/commit/9f3a43ec1a8df527ed3f6f81c61a23980bb4c088))

- **generation**: Update generated SDK [skip ci]
  ([`5de8f5b`](https://github.com/camunda/orchestration-cluster-api-python/commit/5de8f5ba9875523546cd3205755dfe762000e3b4))

- **generation**: Update generated SDK [skip ci]
  ([`ff730f0`](https://github.com/camunda/orchestration-cluster-api-python/commit/ff730f05b1c4480be132bfcde75525ce2af916ec))

- **generation**: Update generated SDK [skip ci]
  ([`d792035`](https://github.com/camunda/orchestration-cluster-api-python/commit/d79203543e18edc7c02e8abd38f764b87d37f5e2))

- **generation**: Update generated SDK [skip ci]
  ([`48c793e`](https://github.com/camunda/orchestration-cluster-api-python/commit/48c793ecb421b84f4bbef71b5cbdf8bfcc3b473d))

- **generation**: Update generated SDK [skip ci]
  ([`5186476`](https://github.com/camunda/orchestration-cluster-api-python/commit/518647611e7de4b0b7f204ef99fc04447e958c14))

- **generation**: Update generated SDK [skip ci]
  ([`3101d25`](https://github.com/camunda/orchestration-cluster-api-python/commit/3101d25913e3e32c0a2ca6ea9f90623198fecc54))

- **generation**: Update generated SDK [skip ci]
  ([`a6ac683`](https://github.com/camunda/orchestration-cluster-api-python/commit/a6ac683e43a5204f798bda3e1989e04925d66a48))

### Code Style

- Lint all code
  ([`db876bb`](https://github.com/camunda/orchestration-cluster-api-python/commit/db876bb4c197d5f0a3bece6193dcd882a790289e))

- Reformat with normalised format
  ([`6d659f2`](https://github.com/camunda/orchestration-cluster-api-python/commit/6d659f2d75efdf68d18bdf97a38f874b66e2e44a))

### Documentation

- Add admonition to README for maintainer awareness
  ([`038ec29`](https://github.com/camunda/orchestration-cluster-api-python/commit/038ec29cca07ee37e379702036b125b98d0169c6))

- Add md-doc support for Docusaurus
  ([`394bda0`](https://github.com/camunda/orchestration-cluster-api-python/commit/394bda025ddcfae45b30b7a1675cda8eb74c012f))

- Reorder README sections for Docusaurus integration
  ([`11a2f56`](https://github.com/camunda/orchestration-cluster-api-python/commit/11a2f56c7472129a5f8087dcc2f19b83a43245a0))

- Reorganise for Docusaurus
  ([`c8bb4af`](https://github.com/camunda/orchestration-cluster-api-python/commit/c8bb4af84d3793b26aa9d1f6f9ab91a7773d9cca))

- Support Docusaurus integration
  ([`b6b74cf`](https://github.com/camunda/orchestration-cluster-api-python/commit/b6b74cf8c4996ac6ce0d0e9f1cf70deed83211b2))

- Support Docusaurus link requirements
  ([`83077b3`](https://github.com/camunda/orchestration-cluster-api-python/commit/83077b35d08b5fb9a29d06aa370bee2df3c4280f))

- Update Docusaurus integration
  ([`a90ae7f`](https://github.com/camunda/orchestration-cluster-api-python/commit/a90ae7fbca3711d3a4e654f37f51956e95cc6448))

- Use modified README as landing page in Docusaurus
  ([`8eacc97`](https://github.com/camunda/orchestration-cluster-api-python/commit/8eacc97e2ad086451bc1be59b7b6577a73be2d66))


## v8.9.0-dev.6 (2026-02-15)

### Bug Fixes

- Fix errors in type declarations
  ([`0d3a0b6`](https://github.com/camunda/orchestration-cluster-api-python/commit/0d3a0b6234357d9aa8d7af9dee4dc7c231e077fe))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`99c3c8b`](https://github.com/camunda/orchestration-cluster-api-python/commit/99c3c8babb56378564d3d9884dfb5463569c84f5))

- **generation**: Update generated SDK [skip ci]
  ([`64bd5aa`](https://github.com/camunda/orchestration-cluster-api-python/commit/64bd5aa617eef85c0b318cdc3072880fcad445ec))

### Documentation

- Add note on versioning and breaking changes
  ([`8abaf62`](https://github.com/camunda/orchestration-cluster-api-python/commit/8abaf627a3c67576da3ad39e1c64b896e9b5db5e))

### Features

- Add typing declarations
  ([`b65b72f`](https://github.com/camunda/orchestration-cluster-api-python/commit/b65b72fba66cdae24c01ba138a871090b0ef30ef))


## v8.9.0-dev.5 (2026-02-14)

### Bug Fixes

- Lift path params to semantic types
  ([`886ca70`](https://github.com/camunda/orchestration-cluster-api-python/commit/886ca7070e2976419d95d28a6ef80197a0eb849f))

- Use camunda-schema-bundler for generation
  ([`9e50ea1`](https://github.com/camunda/orchestration-cluster-api-python/commit/9e50ea1e6c9b04714f6b87e76af3dd3c3bedb88c))

### Chores

- Fix config reference generator for logging config
  ([`8ad5cb5`](https://github.com/camunda/orchestration-cluster-api-python/commit/8ad5cb5f8503b495474bfba8b0249c8c80c0c8f0))

- **generation**: Update generated SDK [skip ci]
  ([`2a98370`](https://github.com/camunda/orchestration-cluster-api-python/commit/2a983709c36b8b4de07548222fb42eea2369a80d))

### Code Style

- Format code
  ([`eba92de`](https://github.com/camunda/orchestration-cluster-api-python/commit/eba92deb453195723c869e483deb70199bdcf1dc))

### Continuous Integration

- Use camunda-schema-bundler binary
  ([`64a6275`](https://github.com/camunda/orchestration-cluster-api-python/commit/64a6275d39a8dcb0c5ce3230a450853e1544d7f4))

- Use npx for camunda-schema-bundler
  ([`5908320`](https://github.com/camunda/orchestration-cluster-api-python/commit/59083203879cbf71f7170536a39f80bcd9471c05))

### Documentation

- Add link to docs
  ([`c6e13b4`](https://github.com/camunda/orchestration-cluster-api-python/commit/c6e13b4cc0bf9d4f1c5e09adf939a375ecb5de99))

- Add type-checked examples
  ([`4daac2d`](https://github.com/camunda/orchestration-cluster-api-python/commit/4daac2dfbb0d5bec34fb08e74cdcddc5a7470702))

- Explain Sync and Async clients
  ([`2355c82`](https://github.com/camunda/orchestration-cluster-api-python/commit/2355c82a6806c60b141918d76c70b250f4bed75f))

- Generate docs with Sphinx
  ([`b2782f3`](https://github.com/camunda/orchestration-cluster-api-python/commit/b2782f30308120d893194d29f779116f1f18504b))

- Inject examples into generated code
  ([`94a5bf3`](https://github.com/camunda/orchestration-cluster-api-python/commit/94a5bf360c2d94c322a0148400c135cf81607927))

- Minor edit
  ([`9c3d6a3`](https://github.com/camunda/orchestration-cluster-api-python/commit/9c3d6a3997349a69329b521210d2a15dfa9e90a4))

### Features

- Add custom logging support
  ([`0c29eac`](https://github.com/camunda/orchestration-cluster-api-python/commit/0c29eacaa2aff9e1f98d430e4564fc4a83e2a05a))

- Add logger to worker JobContext
  ([`e9f742c`](https://github.com/camunda/orchestration-cluster-api-python/commit/e9f742c21bd4859e70075a8056953cc755427130))


## v8.9.0-dev.4 (2026-02-12)

### Bug Fixes

- Add configuration reference to README
  ([`3647014`](https://github.com/camunda/orchestration-cluster-api-python/commit/3647014d242a0776a1ef10d2e7a223d60588a0ed))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`1ca35cf`](https://github.com/camunda/orchestration-cluster-api-python/commit/1ca35cf5486ad4d1878447e393045133fc28ae63))

### Continuous Integration

- Add hint to workflow
  ([`6bd3b08`](https://github.com/camunda/orchestration-cluster-api-python/commit/6bd3b082e236a432d33dbb66b86ef0b417ffac79))


## v8.9.0-dev.3 (2026-02-12)

### Bug Fixes

- Update test coverage and docs
  ([`0e4f495`](https://github.com/camunda/orchestration-cluster-api-python/commit/0e4f495465c3319e23470cc9364e2367b3dba596))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`466c825`](https://github.com/camunda/orchestration-cluster-api-python/commit/466c825d37e2025ccf8cfcf088032703c17fdb97))


## v8.9.0-dev.2 (2026-02-12)

### Bug Fixes

- Strictly type check SDK
  ([`c1693cf`](https://github.com/camunda/orchestration-cluster-api-python/commit/c1693cfccc7f7cf99322d51f26fb716911825b0a))

### Chores

- Generated code
  ([`65b15b7`](https://github.com/camunda/orchestration-cluster-api-python/commit/65b15b7c93a1a5718114c2b84d0cf434ee5fb27b))

- Regenerate
  ([`e055b7e`](https://github.com/camunda/orchestration-cluster-api-python/commit/e055b7e7cb5814e2a82bf8620aa44fe5269d1fe4))

- Strict type checking
  ([`40bf35c`](https://github.com/camunda/orchestration-cluster-api-python/commit/40bf35c5f29c5472b42985de45ae1a4bd368ef60))

- **generation**: Update generated SDK [skip ci]
  ([`cf1495f`](https://github.com/camunda/orchestration-cluster-api-python/commit/cf1495fd3c0d15bf0973aad6bcf3f4cb569305b6))

- **generation**: Update generated SDK [skip ci]
  ([`7e3fd9b`](https://github.com/camunda/orchestration-cluster-api-python/commit/7e3fd9b91ee17e0b1a55fbeb3f60e4ab6b6ad1c1))

### Refactoring

- Address review feedback
  ([`95e28c9`](https://github.com/camunda/orchestration-cluster-api-python/commit/95e28c9e6bea1c9c44f91fdfec7f7afe5534ab08))

- Fix linting error
  ([`9dbd7da`](https://github.com/camunda/orchestration-cluster-api-python/commit/9dbd7daeea0fff98d40a3b342f5cf98105085dd7))


## v1.2.0-dev.1 (2026-02-11)

### Chores

- Add default excludes
  ([`6948418`](https://github.com/camunda/orchestration-cluster-api-python/commit/6948418cd488a362a646ad177d42b4720b08fc8f))

- Branch automatically constrains version
  ([`aa202e1`](https://github.com/camunda/orchestration-cluster-api-python/commit/aa202e172be816637b28f14263ec26c7947860f3))

- Change prerelease token to dev
  ([`363b209`](https://github.com/camunda/orchestration-cluster-api-python/commit/363b209bcea53666daff85a174c7b362bbf649b1))

- Fix linting
  ([`2251c0f`](https://github.com/camunda/orchestration-cluster-api-python/commit/2251c0f183d1cd3338efe88bab92421ec4ef1560))

- Set up packaging workflow
  ([`c4730b5`](https://github.com/camunda/orchestration-cluster-api-python/commit/c4730b5d7df91c511a4ef6f2e3db7fc64284724b))

- **generation**: Update generated SDK [skip ci]
  ([`84acdca`](https://github.com/camunda/orchestration-cluster-api-python/commit/84acdcac9ad6ac144382e87b2f09c369a0d339e7))

### Continuous Integration

- Align publishing
  ([`6948b1f`](https://github.com/camunda/orchestration-cluster-api-python/commit/6948b1f395c2b56e8d9e6fd4e002cff483fd1224))

- Test on 3.10 and 3.14
  ([`dab6863`](https://github.com/camunda/orchestration-cluster-api-python/commit/dab6863320cdd1ae610771c03df245a6893bfe16))

### Refactoring

- Address review comments
  ([`73c0636`](https://github.com/camunda/orchestration-cluster-api-python/commit/73c06368af0df8286864345056de55f648b52ad7))

### Server

- Start 8.9 prerelease line
  ([`b507169`](https://github.com/camunda/orchestration-cluster-api-python/commit/b507169159af106ffe0888fef5ac7c14339dc116))


## v1.1.3 (2026-02-11)

### Bug Fixes

- Declare 3.10 support
  ([`8bd3d52`](https://github.com/camunda/orchestration-cluster-api-python/commit/8bd3d52bb14a435ca0f0b463193615cae71c04ad))

- Docs deployment. fixes #47
  ([`92684ef`](https://github.com/camunda/orchestration-cluster-api-python/commit/92684ef1c794f013133958849261e643dcba7e04))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`021e4e6`](https://github.com/camunda/orchestration-cluster-api-python/commit/021e4e68e8c176225a1303dcee4c20f0662cec38))


## v1.1.2 (2026-02-10)

### Bug Fixes

- Correctly set version during publish
  ([`ec19cd8`](https://github.com/camunda/orchestration-cluster-api-python/commit/ec19cd875adc798506c5111381130d217e009850))

### Chores

- Ignore egg-info
  ([`b460431`](https://github.com/camunda/orchestration-cluster-api-python/commit/b46043154fd90e8551fe79980b9879a89f119d92))

- **generation**: Update generated SDK [skip ci]
  ([`62ae279`](https://github.com/camunda/orchestration-cluster-api-python/commit/62ae2793f9e907c51e3b1be459fedf9a68495c83))


## v1.1.1 (2026-02-10)

### Bug Fixes

- Apply review feedback and regenerate
  ([`6262d85`](https://github.com/camunda/orchestration-cluster-api-python/commit/6262d8594bb94266cf3932ac2d80a24fd9424b3c))

### Chores

- Add configuration resolver
  ([`04a34c9`](https://github.com/camunda/orchestration-cluster-api-python/commit/04a34c9ef61c88e47700dff3cd8a79f850b3ae2c))

- Add opt-in env file loading
  ([`f812867`](https://github.com/camunda/orchestration-cluster-api-python/commit/f812867e841b20bc0f4e878d6b96c43615389dab))

- Avoid tar pit on SaaS
  ([`0708b6b`](https://github.com/camunda/orchestration-cluster-api-python/commit/0708b6b9873386269c245cfe84d684291a14ddaa))

- Deploy on push to main
  ([`c50076e`](https://github.com/camunda/orchestration-cluster-api-python/commit/c50076e8f7c6be40c0fb89bcee8f8fc25d7ecb57))

- Emit debug statement on exception
  ([`5340503`](https://github.com/camunda/orchestration-cluster-api-python/commit/5340503a89f3c57fc0fdbbeb625afeacb535a444))

- Enhance exception documentation
  ([`09b9dd7`](https://github.com/camunda/orchestration-cluster-api-python/commit/09b9dd723a310fcd2014fd1c8ff4a76aa4a2f4d7))

- Fix no httpx module
  ([`3892443`](https://github.com/camunda/orchestration-cluster-api-python/commit/3892443120796d2d4befe7e96a36362a55f9041f))

- Fixes to doc generation
  ([`8bd4b76`](https://github.com/camunda/orchestration-cluster-api-python/commit/8bd4b7679530993b640507ba5840e8b5c106281b))

- Implement OAuth
  ([`1609caf`](https://github.com/camunda/orchestration-cluster-api-python/commit/1609caff45c005173fa7f0abeea73a24c005a3d0))

- Implement OAuth and Basic auth
  ([`fc1c6d2`](https://github.com/camunda/orchestration-cluster-api-python/commit/fc1c6d24541b28f44a8b1ab067d4e668df838f2f))

- Implement pluggable auth
  ([`8c9ab6f`](https://github.com/camunda/orchestration-cluster-api-python/commit/8c9ab6ff2e1470756d559acd2a033cffa5e992bf))

- Install all dependencies for pdocs
  ([`03a8c7c`](https://github.com/camunda/orchestration-cluster-api-python/commit/03a8c7c5b1e6d69cd936f15d8824213f6821dd46))

- Install root dependencies
  ([`0106422`](https://github.com/camunda/orchestration-cluster-api-python/commit/010642236cbb88ed7a52ec5447dc006e9cdcf78b))

- Set environment for github
  ([`2f7f8e0`](https://github.com/camunda/orchestration-cluster-api-python/commit/2f7f8e083d59dc6651ba6c142a5f45aa8023b0a5))

- Split client to sync and async
  ([`51ca5d5`](https://github.com/camunda/orchestration-cluster-api-python/commit/51ca5d56813a9a6edbb2e896775662fc0764e690))

- Update week_2 demo
  ([`c6cc041`](https://github.com/camunda/orchestration-cluster-api-python/commit/c6cc041ee520a27bf56e34d94556202f64b252c7))

- Wip
  ([`316908f`](https://github.com/camunda/orchestration-cluster-api-python/commit/316908fa20e9e64deb1c8b73e2ec1b1baf36f14f))

- **generation**: Update generated SDK [skip ci]
  ([`915833c`](https://github.com/camunda/orchestration-cluster-api-python/commit/915833c84aa2e13336a6d7b10ac63c79e978a3d3))

### Continuous Integration

- Support temporary spec override via env vars
  ([`1cf17a0`](https://github.com/camunda/orchestration-cluster-api-python/commit/1cf17a0869f0cbd74e695a7b268793cc84795a50))

### Documentation

- Add comment to exception swallowing
  ([`3e63fe2`](https://github.com/camunda/orchestration-cluster-api-python/commit/3e63fe284b15742017cdebf4f480966e8c3800b5))

- Document deploy_resources_from_files
  ([`a443e55`](https://github.com/camunda/orchestration-cluster-api-python/commit/a443e551501d45a0dba4927023be1935f508a8df))

- Remove forward reference of JobContext
  ([`531d138`](https://github.com/camunda/orchestration-cluster-api-python/commit/531d138d4aa7f3e83eee67591c8363a16ec019dc))

- Update docs/provided-auth-strategies.md
  ([`e3d298b`](https://github.com/camunda/orchestration-cluster-api-python/commit/e3d298ba963a51899d80e9339dbe4feb19b5efb0))

- Update documentation
  ([`35067af`](https://github.com/camunda/orchestration-cluster-api-python/commit/35067afe7f5c6ba4a9662e649a0cb3e020f1b2db))

### Refactoring

- Fix type errors
  ([`94f44a4`](https://github.com/camunda/orchestration-cluster-api-python/commit/94f44a41cc0c4f8eeaa7cf0af86a024a2afed4ad))


## v1.1.0 (2026-01-13)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`b4be73a`](https://github.com/camunda/orchestration-cluster-api-python/commit/b4be73aa7bef594db74537077bf48bde26e4b685))

### Features

- Deploy docs to github
  ([`997aa2b`](https://github.com/camunda/orchestration-cluster-api-python/commit/997aa2b07628a6ab8a014d0c11e4c1749ccb8c3e))

- Use pdoc to generate docs-api
  ([`ceaf5a8`](https://github.com/camunda/orchestration-cluster-api-python/commit/ceaf5a8757b683b41e21633e097fb4b3e64e1bad))


## v1.0.1 (2026-01-13)

### Bug Fixes

- Add request_timeout to job worker
  ([`53d9cb4`](https://github.com/camunda/orchestration-cluster-api-python/commit/53d9cb4d4ddfb2fc2d0d5b6a33c432a2618ef714))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`8224165`](https://github.com/camunda/orchestration-cluster-api-python/commit/8224165fd486b6d4366f3ed6620de3c4cadb1deb))


## v1.0.0 (2026-01-08)

- Initial Release
