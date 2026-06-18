# CHANGELOG

<!-- version list -->

## v10.1.0-dev.17 (2026-06-18)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`fbef76f`](https://github.com/camunda/orchestration-cluster-api-python/commit/fbef76f4c5946afa32a51a9eb00ee7e5b1ae98f3))

### Features

- Regenerate SDK for job priority-updated state and timer/signal wait-states
  ([`e638974`](https://github.com/camunda/orchestration-cluster-api-python/commit/e6389749e1daa054c931254dc9e452ea7e7cb58d))


## v10.1.0-dev.16 (2026-06-11)

### Bug Fixes

- **gen**: Drop discriminator-only oneOf union base models
  ([`a39819b`](https://github.com/camunda/orchestration-cluster-api-python/commit/a39819b2021ff1ca2d79ec312a23d5ddea6f330e))

- **gen**: Handle multi-line imports + add tests for orphan-base hook
  ([`75cebdf`](https://github.com/camunda/orchestration-cluster-api-python/commit/75cebdf346720e5a125f3aa53ca8ae72f2728f9a))

- **gen**: Make orphan-base hook pass ty type check
  ([`fba027e`](https://github.com/camunda/orchestration-cluster-api-python/commit/fba027ea373491048913a6e25206ec4761cfeec5))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`beef6f7`](https://github.com/camunda/orchestration-cluster-api-python/commit/beef6f763a935e9ad88e0c5e3f73e8ba75299243))


## v10.1.0-dev.15 (2026-06-11)

### Bug Fixes

- Adopt upstream wait-state details union in example
  ([`7da1406`](https://github.com/camunda/orchestration-cluster-api-python/commit/7da1406196c95ef689b1461a1f870ffa473f2296))

- Drop unused MessageWaitStateDetails import
  ([`9516103`](https://github.com/camunda/orchestration-cluster-api-python/commit/951610364c5d32aafc0dbdbc2f3812ad1675f8bf))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`7db35c4`](https://github.com/camunda/orchestration-cluster-api-python/commit/7db35c4254ba0d6ac45c963cbc9fcd3e28ff47d0))


## v10.1.0-dev.14 (2026-06-10)

### Chores

- **generation**: Regenerate SDK for collection-level variable consistency wait
  ([`00daf98`](https://github.com/camunda/orchestration-cluster-api-python/commit/00daf986d24d23047c511501dbf423da3cbfe44b))

- **generation**: Regenerate SDK for DTO-driven typed variable maps
  ([`8f30f8e`](https://github.com/camunda/orchestration-cluster-api-python/commit/8f30f8e8efd1360c1bf3607bdd919b98d67b17e7))

- **generation**: Update generated SDK [skip ci]
  ([`7f20fc7`](https://github.com/camunda/orchestration-cluster-api-python/commit/7f20fc70fbcf2cc71a13c5271759ec51c553d0e7))

### Documentation

- Add search_variables_as_dto usage example
  ([`0350bcf`](https://github.com/camunda/orchestration-cluster-api-python/commit/0350bcfc2b83c960523f81e73c3db0db5d1939e1))

### Features

- Add DTO-driven typed variable maps (search_variables_as_dto)
  ([`6b8ca44`](https://github.com/camunda/orchestration-cluster-api-python/commit/6b8ca44dfdf05c62ff526b06524d4779131ac8b9))

- Add eventual-consistency wait to search_variables_as_dto
  ([`4236484`](https://github.com/camunda/orchestration-cluster-api-python/commit/4236484d15c8cbe064fdf8446e34b1f3570167bc))

### Refactoring

- Keep typed-variable search memory-bounded and fix VariableMap stubs
  ([`2c18af7`](https://github.com/camunda/orchestration-cluster-api-python/commit/2c18af7ddf7b4650700f269ea0a72b15f97be7c4))


## v10.1.0-dev.13 (2026-06-09)

### Bug Fixes

- Handle integer semantic keys and wrapped list parse helpers in SDK codegen
  ([`04f1fa3`](https://github.com/camunda/orchestration-cluster-api-python/commit/04f1fa3008d8759f2466ddfba52fcdf84a0baf81))

- **deps**: Bump camunda-schema-bundler to 2.4.3
  ([`0db1da3`](https://github.com/camunda/orchestration-cluster-api-python/commit/0db1da3b7d0e9637db88318d4f5f1d52a92f57e9))

### Chores

- Align list-parse guard regex with hook 1200 trailing comma
  ([`ca9476a`](https://github.com/camunda/orchestration-cluster-api-python/commit/ca9476a1b7d6dcb110a2941ffb22ea57860ea48f))

- **generation**: Regenerate SDK for bundler 2.4.3
  ([`7e1ddcb`](https://github.com/camunda/orchestration-cluster-api-python/commit/7e1ddcbadd6b00bcfc2ccb2a47d1af2fbf961c11))

- **generation**: Update generated SDK [skip ci]
  ([`fe0d492`](https://github.com/camunda/orchestration-cluster-api-python/commit/fe0d4921321be6b3068ce7437c3796c7796e8ec6))

### Documentation

- Add examples for agent instance history operations
  ([`350a3e2`](https://github.com/camunda/orchestration-cluster-api-python/commit/350a3e206aa2daf176b04b3c3637827b75cf3868))


## v10.1.0-dev.12 (2026-06-04)

### Bug Fixes

- Pass author-association to community notification workflow
  ([`ea9abe8`](https://github.com/camunda/orchestration-cluster-api-python/commit/ea9abe8c11e0e74faddf400e332a4c10d071f8a9))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`5c8691e`](https://github.com/camunda/orchestration-cluster-api-python/commit/5c8691e5ec1af049895c50ce98b7db13b77d5eb6))

### Continuous Integration

- Pass vault secrets for org membership check
  ([`72e4c16`](https://github.com/camunda/orchestration-cluster-api-python/commit/72e4c16f1a7d7da2b7610062e11fd7361d15f254))


## v10.1.0-dev.11 (2026-06-04)

### Chores

- Add priority field to test constructors
  ([`c5dbd9f`](https://github.com/camunda/orchestration-cluster-api-python/commit/c5dbd9f97fdf54459af6ea8904e43dd61719bee2))

- Update bundled spec to latest upstream
  ([`bc6f0dd`](https://github.com/camunda/orchestration-cluster-api-python/commit/bc6f0dd2f9f2ceb18e541ef553153d52ca08389b))

- Upgrade test docker image to 8.10-SNAPSHOT
  ([`5df76de`](https://github.com/camunda/orchestration-cluster-api-python/commit/5df76de812e41d49bbb3769c93e24f799a7871bb))

- **generation**: Regenerate SDK for job worker improvements
  ([`9f1a2fb`](https://github.com/camunda/orchestration-cluster-api-python/commit/9f1a2fbdd9236c5890c83ed16d710a81baa8ee2d))

- **generation**: Regenerate SDK for upstream spec update
  ([`d22d803`](https://github.com/camunda/orchestration-cluster-api-python/commit/d22d80330dd5f80154838b84101557b18075fc40))

- **generation**: Update generated SDK [skip ci]
  ([`d84cd5d`](https://github.com/camunda/orchestration-cluster-api-python/commit/d84cd5d173a098f41bc7e9fe89dc4b2cb54a10bd))

- **generation**: Update generated SDK [skip ci]
  ([`419dba5`](https://github.com/camunda/orchestration-cluster-api-python/commit/419dba5b3ca8cca4af7298d636aa704843a8c14d))

### Continuous Integration

- Remove temporary test workflow [skip ci]
  ([`69beb85`](https://github.com/camunda/orchestration-cluster-api-python/commit/69beb85de35d355a37782da70c8f4049eba89d71))

- Temporary test workflow for org membership API [skip ci]
  ([`0dc4c0e`](https://github.com/camunda/orchestration-cluster-api-python/commit/0dc4c0e9ae2cfdfdf7b1e0088841da1598a36b60))

### Features

- Improve job worker autocomplete, variables, and logging
  ([`b8a5001`](https://github.com/camunda/orchestration-cluster-api-python/commit/b8a500124abd5789658ce53c312529c91290b4de))


## v10.1.0-dev.10 (2026-05-29)

### Chores

- **generation**: Regenerate SDK for default-tenant-ids injection
  ([`ff4b8d0`](https://github.com/camunda/orchestration-cluster-api-python/commit/ff4b8d03f725139d48931e812ebd8124cd1320c6))

### Features

- **runtime**: Default CAMUNDA_TENANT_ID(S) into request bodies with optional tenantIds[]
  ([`8587a89`](https://github.com/camunda/orchestration-cluster-api-python/commit/8587a8944998a2421687c4100aa71fd070612846))


## v10.1.0-dev.9 (2026-05-28)

### Bug Fixes

- **runtime**: Track in-flight job tasks so stop()/aclose() can cancel them
  ([`c85d09f`](https://github.com/camunda/orchestration-cluster-api-python/commit/c85d09f5cf3c78379d23a80140b9eefaf7173e11))

### Chores

- Address review comments on PR #152
  ([`3e1bdba`](https://github.com/camunda/orchestration-cluster-api-python/commit/3e1bdba64fd461c857e3f1c8e9cbca266385bbc6))

- Address review comments on PR #152 (round 2)
  ([`5b7e186`](https://github.com/camunda/orchestration-cluster-api-python/commit/5b7e186fa31daeef65c6c8ca3f44d880a023dc64))

- **generation**: Regenerate SDK for in-flight task tracking + review fixes
  ([`f4853dc`](https://github.com/camunda/orchestration-cluster-api-python/commit/f4853dc56ac8f21c467b1fbf6fdd45f464954325))

- **generation**: Update generated SDK [skip ci]
  ([`5868916`](https://github.com/camunda/orchestration-cluster-api-python/commit/58689163cb4096fbc4be5a4161409dcdb68c04ae))


## v10.1.0-dev.8 (2026-05-28)

### Bug Fixes

- **runtime**: Lazy-allocate JobWorker pools and event loop
  ([`d874ef8`](https://github.com/camunda/orchestration-cluster-api-python/commit/d874ef8ba9bb9453d15b21d556f11324aa0b3d6e))

### Chores

- Address review comments on close() lifecycle hazards
  ([`e8ec23b`](https://github.com/camunda/orchestration-cluster-api-python/commit/e8ec23bc89e064bea9d6b800dfdbfd72291189e4))

- Address review comments on JobWorker.close/stop
  ([`2d48189`](https://github.com/camunda/orchestration-cluster-api-python/commit/2d481894e43d37dfc77b60637f3c5986c60705e1))

- Address review comments on lazy-init concurrency + test scope
  ([`6f5e5c3`](https://github.com/camunda/orchestration-cluster-api-python/commit/6f5e5c39a5122e9bbdaea8074b8db579fb7fdc95))

- Harden JobWorker close() against more lifecycle hazards
  ([`39d3995`](https://github.com/camunda/orchestration-cluster-api-python/commit/39d3995baced541fca8a7dd30a18d20978681fc0))

- **generation**: Regenerate SDK for JobWorker lazy pools + close() hardening
  ([`43c910c`](https://github.com/camunda/orchestration-cluster-api-python/commit/43c910c62f2508b97423e179bd933da89e345948))

- **generation**: Update generated SDK [skip ci]
  ([`de6b0cf`](https://github.com/camunda/orchestration-cluster-api-python/commit/de6b0cff88fb1766da1efa8387812e5b687643ac))


## v10.1.0-dev.7 (2026-05-28)

### Chores

- Add permissions: {} to community-notify workflow
  ([`7a4a23b`](https://github.com/camunda/orchestration-cluster-api-python/commit/7a4a23bb13f7fe26793bc1747c24d7b53781da00))

- **generation**: Update generated SDK [skip ci]
  ([`bf8733c`](https://github.com/camunda/orchestration-cluster-api-python/commit/bf8733c75a4a3c9fa97c812b0a46adffac2978d2))

### Features

- Add Slack notifications for release failures and community events
  ([`ee1e865`](https://github.com/camunda/orchestration-cluster-api-python/commit/ee1e86597ec3e6217272548f781d3f114aa74740))


## v10.1.0-dev.6 (2026-05-28)

### Chores

- Address review comments
  ([`3a2d417`](https://github.com/camunda/orchestration-cluster-api-python/commit/3a2d417789f6b3854022842a5cdc061978b47b2f))

- Remove demo/ directory
  ([`0606bc1`](https://github.com/camunda/orchestration-cluster-api-python/commit/0606bc126fa03c69e49c08b21646e3a0a291684e))

- **generation**: Regenerate SDK for ty migration
  ([`d6ae7e4`](https://github.com/camunda/orchestration-cluster-api-python/commit/d6ae7e4189d986b9b35e232260a13f5eb5609234))

- **generation**: Update generated SDK [skip ci]
  ([`b9fe173`](https://github.com/camunda/orchestration-cluster-api-python/commit/b9fe1733c61b583b58236bd0d01f3d63cb59bc7a))

### Features

- **typecheck**: Migrate from pyright to ty
  ([`bdcd7c6`](https://github.com/camunda/orchestration-cluster-api-python/commit/bdcd7c63ceb74d82aca8397fead50cf36b65712b))


## v10.1.0-dev.5 (2026-05-28)

### Bug Fixes

- **hooks**: Annotate 3-variant _parse_* helper for optional+nullable list-of-model
  ([`921826f`](https://github.com/camunda/orchestration-cluster-api-python/commit/921826f2d1a6e9acf70f16c03005f2f544785760))

- **hooks**: Annotate to_dict accumulator for required, non-nullable list of polymorphic oneOf
  ([`ab920ad`](https://github.com/camunda/orchestration-cluster-api-python/commit/ab920ad5a68a1e4e2cdc07b01dd442f8b4b60cf7))

### Build System

- **deps**: Bump actions/upload-pages-artifact from 4 to 5
  ([`228231a`](https://github.com/camunda/orchestration-cluster-api-python/commit/228231a665e75b4cd67f185e027191e813f34360))

- **deps**: Update loguru requirement from >=0.7.2 to >=0.7.3
  ([`c8f502b`](https://github.com/camunda/orchestration-cluster-api-python/commit/c8f502ba4d5b813cc55789c2b2c20a00780f0fc9))

- **deps-dev**: Update fastapi requirement from >=0.128.0 to >=0.135.3
  ([`355b94a`](https://github.com/camunda/orchestration-cluster-api-python/commit/355b94ac2e759ee081135f921b3a76903d07cca5))

- **deps-dev**: Update pyright requirement from >=1.1.407 to >=1.1.408
  ([`ccb7e1e`](https://github.com/camunda/orchestration-cluster-api-python/commit/ccb7e1ee03de842bf5894d1c1b9ea27fdbc0e961))

### Chores

- Add always() and secret guard to notify job
  ([`54178ef`](https://github.com/camunda/orchestration-cluster-api-python/commit/54178ef96c9011914587900effbe6d44c5bc1a6c))

- Add empty permissions to notify job
  ([`c4a2ca4`](https://github.com/camunda/orchestration-cluster-api-python/commit/c4a2ca46547a43009d390b678e898da0e89324d6))

- Remove secrets guard from job-level if expression
  ([`811fee6`](https://github.com/camunda/orchestration-cluster-api-python/commit/811fee6e4dba08cc1734552154a7c9af242cc59f))

- **deps**: Bump actions/download-artifact from 4 to 8
  ([`420202a`](https://github.com/camunda/orchestration-cluster-api-python/commit/420202a2541abdb656534590ae2e772b0e5b7458))

- **generation**: Regenerate SDK for hook 1200 + example fixes
  ([`4a2630a`](https://github.com/camunda/orchestration-cluster-api-python/commit/4a2630aab0e5753d0a7b1756ce5f77605fe237e5))

- **generation**: Update generated SDK [skip ci]
  ([`f46a1a9`](https://github.com/camunda/orchestration-cluster-api-python/commit/f46a1a912094f176b524fbe1184c120e260a69b2))

- **generation**: Update generated SDK [skip ci]
  ([`ed54262`](https://github.com/camunda/orchestration-cluster-api-python/commit/ed54262be9d06514ebe7b0f8007c5e5ce73b90f9))

- **generation**: Update generated SDK [skip ci]
  ([`c16ebb5`](https://github.com/camunda/orchestration-cluster-api-python/commit/c16ebb5633b85a8e3c872b2d50c995467922c0e2))

- **generation**: Update generated SDK [skip ci]
  ([`3dd2104`](https://github.com/camunda/orchestration-cluster-api-python/commit/3dd210400d6bd05c065edc84836b0b88524b4438))

- **generation**: Update generated SDK [skip ci]
  ([`bf75c8e`](https://github.com/camunda/orchestration-cluster-api-python/commit/bf75c8ed55bd188e1bfa8e5be8e1baf4501db10f))

- **generation**: Update generated SDK [skip ci]
  ([`d09b759`](https://github.com/camunda/orchestration-cluster-api-python/commit/d09b759d9907e730296a17eb3772ce00b5625c94))

- **generation**: Update generated SDK [skip ci]
  ([`93f1a18`](https://github.com/camunda/orchestration-cluster-api-python/commit/93f1a18b9a64793c22824158fe91346f206266e9))

### Continuous Integration

- Add breaking change guard to PR workflow
  ([`806ee29`](https://github.com/camunda/orchestration-cluster-api-python/commit/806ee293a3b9e5081fd0ef82c1ce6fb5766f32c1))

- Add Slack notification on release failure
  ([`7090cd3`](https://github.com/camunda/orchestration-cluster-api-python/commit/7090cd3bd708c361bd3fbe7d2facf1310dac43d2))

- Retrigger workflow with updated sdk-infra v1 tag
  ([`612ff99`](https://github.com/camunda/orchestration-cluster-api-python/commit/612ff99bc29278c8d2161ab1fd95aa149ff5e9d4))

### Documentation

- **examples**: Add example for searchElementInstanceWaitStates
  ([`439ba24`](https://github.com/camunda/orchestration-cluster-api-python/commit/439ba240d9c42a8f7b1ff3cc85417c030409b6af))


## v10.1.0-dev.4 (2026-05-13)

### Bug Fixes

- Add Http406Error (NotAcceptableError) to error class mappings
  ([`cea4b92`](https://github.com/camunda/orchestration-cluster-api-python/commit/cea4b92bb5eb23c3a3eff2f02101af8d1620c882))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`482851c`](https://github.com/camunda/orchestration-cluster-api-python/commit/482851cc551b14dcbae96c4db0d8facd04145157))

### Features

- Add example coverage for 4 new operations
  ([`b58f85c`](https://github.com/camunda/orchestration-cluster-api-python/commit/b58f85c8f89bdda76e38ae7c8bf98f40900baab9))


## v10.1.0-dev.3 (2026-05-10)

### Bug Fixes

- Handle deprecated aliases and __getattr__ in stub generator
  ([`130dd20`](https://github.com/camunda/orchestration-cluster-api-python/commit/130dd2079508671f40c1c13cf2fb6b15117fa383))

- Include stubs/ in ruff format step for deterministic output
  ([`8ac3563`](https://github.com/camunda/orchestration-cluster-api-python/commit/8ac35633f12ce8bfedc4569246c81a9735563483))

### Chores

- Address review comments
  ([`ffdf560`](https://github.com/camunda/orchestration-cluster-api-python/commit/ffdf560a4b105890324132193606c24e3a79ca59))

- Address review comments — fix __all__ comment and use word-boundary validation
  ([`7873328`](https://github.com/camunda/orchestration-cluster-api-python/commit/7873328f1eb32d9bc6fe65a2bb8c2354d0f6238f))

- Address review comments — fix docstring wording and isinstance test
  ([`ecb19eb`](https://github.com/camunda/orchestration-cluster-api-python/commit/ecb19eb46af1cfa09f2456001e80e56164cccb6f))

- Address review comments — fix top-level init docstring
  ([`60a1d87`](https://github.com/camunda/orchestration-cluster-api-python/commit/60a1d875bfc0fa0972586e79ff7477e8c16310f3))

- Rename _rename_map.py to _api_compat_alias_map.py
  ([`cc56105`](https://github.com/camunda/orchestration-cluster-api-python/commit/cc5610536456735291c8d1da0f48eaec39bdde94))

- **generation**: Reformat stubs with ruff for deterministic output
  ([`ff55505`](https://github.com/camunda/orchestration-cluster-api-python/commit/ff5550562965318ed146b174a8bd6b2caf244802))

- **generation**: Regenerate SDK for deprecated type aliases
  ([`fd4bc3b`](https://github.com/camunda/orchestration-cluster-api-python/commit/fd4bc3b0ae1017c4a98e108e66701fb2f073a2f6))

- **generation**: Regenerate stubs with deprecated alias support
  ([`2a07425`](https://github.com/camunda/orchestration-cluster-api-python/commit/2a07425d2c092fb113acccabfc7249a07453d2e9))

- **generation**: Update generated SDK [skip ci]
  ([`8ee6501`](https://github.com/camunda/orchestration-cluster-api-python/commit/8ee650125d2102f1f0e1d865969e69def9b3fdd8))

### Features

- Add backward-compatible deprecated type aliases for v9 model renames
  ([`fd8ca9b`](https://github.com/camunda/orchestration-cluster-api-python/commit/fd8ca9bb334ec543a4cd5cbf9b025bbbb0bd0695))

### Testing

- Add v9 usage pattern regression guards
  ([`2ed70a4`](https://github.com/camunda/orchestration-cluster-api-python/commit/2ed70a45bd7b7176002e84e9fc913441ce1ebb78))


## v10.1.0-dev.2 (2026-05-08)

### Bug Fixes

- Update examples for branded types and add agent instance examples
  ([`b81c24f`](https://github.com/camunda/orchestration-cluster-api-python/commit/b81c24fd67e65de3156e071fa43491ec6d129d3c))

### Chores

- Add type annotations to fix pyright errors in hook
  ([`b9a1b1a`](https://github.com/camunda/orchestration-cluster-api-python/commit/b9a1b1a73d127664a1bf12b091185960e05ad4f7))

- Fix broken repo-relative link in migration section
  ([`36ea4b4`](https://github.com/camunda/orchestration-cluster-api-python/commit/36ea4b493cd5ce487ece6e3e5ba9964809d2735b))

- Fix misleading docstring in semantic type hook
  ([`eb8a4a3`](https://github.com/camunda/orchestration-cluster-api-python/commit/eb8a4a3cd6b20fff3ef4ddced7b6f5561f1b1175))

- Mark stubs and bundled spec as linguist-generated
  ([`f8d0eba`](https://github.com/camunda/orchestration-cluster-api-python/commit/f8d0eba3ac8cd8e65c7c0e84ecd6903c76cd7de5))

- **generation**: Regenerate SDK for branded types and agent instance operations
  ([`1085772`](https://github.com/camunda/orchestration-cluster-api-python/commit/1085772a943de2b8bce1198b8ceeb0436f14bb16))

- **generation**: Regenerate SDK for bundler 2.4.1 and SPEC_REF main
  ([`31cea17`](https://github.com/camunda/orchestration-cluster-api-python/commit/31cea17cf850077e40227957a06c4ef8363f51e4))

- **generation**: Update generated SDK [skip ci]
  ([`cb69a70`](https://github.com/camunda/orchestration-cluster-api-python/commit/cb69a70ea121adaab4ed2bbaccabbede338eda8a))

### Features

- V10 migration — bundler 2.4.1, SPEC_REF main, README migration section
  ([`973d253`](https://github.com/camunda/orchestration-cluster-api-python/commit/973d2531963777967b7a6b9def6b162eead9dc9d))


## v10.1.0-dev.1 (2026-05-05)

### Bug Fixes

- Add missing @commitlint/config-conventional dependency
  ([`f0d5675`](https://github.com/camunda/orchestration-cluster-api-python/commit/f0d56758b27fc7c83f64323fca6dde74baccd06b))

- Add missing searchResources example and fix get_resource_content pyright error
  ([`3403636`](https://github.com/camunda/orchestration-cluster-api-python/commit/3403636efd10e662898a13a7ade8e0238c58b565))

- Guard spec-controlled identifiers against code injection (SFD-214)
  ([`bd03c38`](https://github.com/camunda/orchestration-cluster-api-python/commit/bd03c38a41b59111dc22378e19946446e8857f76))

- Use File.file_name instead of len(File) in example (pyright)
  ([`c5344f6`](https://github.com/camunda/orchestration-cluster-api-python/commit/c5344f6d499d247cb84a61e0fe2db97edc6953c3))

- **eventual**: Keyword-only consistency, create_task, quieter logs, stricter import asserts
  ([`be7a03e`](https://github.com/camunda/orchestration-cluster-api-python/commit/be7a03e04a6524143b0dabd26c84556c52388477))

- **eventual**: Surface 429s to backpressure manager and tighten typing
  ([`87569e8`](https://github.com/camunda/orchestration-cluster-api-python/commit/87569e85632eef57976f60dd0b1bbc632986798e))

### Chores

- Address PR review comments
  ([`2b469ad`](https://github.com/camunda/orchestration-cluster-api-python/commit/2b469aded62943cd45b320e15d7c11f67c3ee2cc))

- Adopt shared sdk-infra commitlint config
  ([`3f15618`](https://github.com/camunda/orchestration-cluster-api-python/commit/3f156185656b3518c1588edbf97e318fbc95378c))

- Append hooks dir to sys.path instead of prepending
  ([`dcc8993`](https://github.com/camunda/orchestration-cluster-api-python/commit/dcc8993562fc423140be5d63fdec9131bc87dd3c))

- Bump @camunda8/sdk-infra to ^1.0.0
  ([`fd7411e`](https://github.com/camunda/orchestration-cluster-api-python/commit/fd7411ec60e8e2fb7766e82ac1abe3c3df75c893))

- Fix ruff lint errors (E402 noqa, unused import)
  ([`5716d80`](https://github.com/camunda/orchestration-cluster-api-python/commit/5716d80b4f3c30779d52b789bcad3d683983eb7a))

- Prevent stale spec fallback, document itest-local, gitignore node_modules
  ([`1088a92`](https://github.com/camunda/orchestration-cluster-api-python/commit/1088a929fe2a928e78063161459a708a6f5b3a5c))

- Trigger CI re-evaluation after sdk-infra went public
  ([`62e51ea`](https://github.com/camunda/orchestration-cluster-api-python/commit/62e51eaae28b17e150e11a4fe5df5dca57707779))

- Update package-lock.json for sdk-infra@1.0.0
  ([`4134af9`](https://github.com/camunda/orchestration-cluster-api-python/commit/4134af9b033d61d4ea585f0fe7914409a16d401c))

- Widen guard param types to object for pyright compatibility
  ([`10de8f3`](https://github.com/camunda/orchestration-cluster-api-python/commit/10de8f3ec8bd8a00500657d99aad9731130de951))

- **generation**: Update generated SDK [skip ci]
  ([`c02d444`](https://github.com/camunda/orchestration-cluster-api-python/commit/c02d444a4eca7c6219fb248d9c6b5ed781c65c59))

- **generation**: Update generated SDK [skip ci]
  ([`1736a6e`](https://github.com/camunda/orchestration-cluster-api-python/commit/1736a6edfbe05bdc758e31a24b367d166d07142f))

- **generation**: Update generated SDK [skip ci]
  ([`152da58`](https://github.com/camunda/orchestration-cluster-api-python/commit/152da5814c3250591c749ad42a2546de60984eb9))

- **generation**: Update generated SDK [skip ci]
  ([`42a7eb5`](https://github.com/camunda/orchestration-cluster-api-python/commit/42a7eb57f080219f7622eb01425ef3ba95a84ef3))

- **generation**: Update generated SDK [skip ci]
  ([`69ec7fb`](https://github.com/camunda/orchestration-cluster-api-python/commit/69ec7fb8528c8c8ed16c98ef5d7261e5e8e70a53))

- **generation**: Update generated SDK [skip ci]
  ([`6b1e6a5`](https://github.com/camunda/orchestration-cluster-api-python/commit/6b1e6a5b1d2efc8f4524131aef81eec0e655c817))

- **generation**: Update generated SDK [skip ci]
  ([`9c14ffa`](https://github.com/camunda/orchestration-cluster-api-python/commit/9c14ffae73bd3a64fb1909f91dec343f6ae5ea41))

### Continuous Integration

- Adopt reusable spec bundling workflow from sdk-infra
  ([`31c1efa`](https://github.com/camunda/orchestration-cluster-api-python/commit/31c1efaa39c13dca78a86c1b6c6e518e4501bdab))

- Adopt start-camunda and stop-camunda composite actions
  ([`1755383`](https://github.com/camunda/orchestration-cluster-api-python/commit/175538363bfcf51fc47567dd6ad2fe56a86ccb23))

- Move typecheck to test job so pyright runs after generate
  ([`b3dbb9e`](https://github.com/camunda/orchestration-cluster-api-python/commit/b3dbb9e8ec7d95b9ca162c96587804e698e12633))

- Replace inline spec-ref guard with reusable sdk-infra workflow
  ([`49fa6c2`](https://github.com/camunda/orchestration-cluster-api-python/commit/49fa6c2e10d11e328eb9235e2dc67a2c5632eecc))

- Retrigger CI
  ([`7649788`](https://github.com/camunda/orchestration-cluster-api-python/commit/7649788615495d104b96b90a432512d1a8b99e3e))

### Documentation

- Fix PSR version format in release docs (use X.Y.Z-dev.N not X.Y.Z.devN)
  ([`d87e933`](https://github.com/camunda/orchestration-cluster-api-python/commit/d87e933556302feec5bedd0d2f698f1d54783664))

- **agents**: Consolidate Copilot instructions into AGENTS.md
  ([`b2a2e74`](https://github.com/camunda/orchestration-cluster-api-python/commit/b2a2e74ada5ff7c5e4d572e9eaebd545e0c3f314))

### Features

- Add transparent eventual consistency polling for annotated endpoints
  ([`12fd924`](https://github.com/camunda/orchestration-cluster-api-python/commit/12fd924dbf9b38db1feff773852e0bb58ecd74e0))

### Testing

- Replace lambda assignment with def to satisfy ruff E731
  ([`f4a2f7b`](https://github.com/camunda/orchestration-cluster-api-python/commit/f4a2f7ba1ecfccf123785cf04b68e37a8d955cb0))


## v8.9.0-dev.39 (2026-04-14)

### Bug Fixes

- **ci**: Pull --rebase before pushing generated changes
  ([`536ad6d`](https://github.com/camunda/orchestration-cluster-api-python/commit/536ad6d96f36b1d481c71bb6305406b6cf0e4c1d))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`c217701`](https://github.com/camunda/orchestration-cluster-api-python/commit/c217701b2683aa4fe068a87633d4911dd1fc60a6))

- **generation**: Update generated SDK [skip ci]
  ([`17c8ccc`](https://github.com/camunda/orchestration-cluster-api-python/commit/17c8ccc73ded31367623268e60674ded7d8e740a))

### Continuous Integration

- Add dependabot entries for stable/9
  ([`509f372`](https://github.com/camunda/orchestration-cluster-api-python/commit/509f3728cf96974d389bfc6a45e8f53b31543939))

### Documentation

- Document PSR major-bump limitation in MAINTAINER.md and RELEASE.md
  ([`01cb5ed`](https://github.com/camunda/orchestration-cluster-api-python/commit/01cb5ed5dd08df193e9142daa15f80694ca52962))


## v8.9.0-dev.38 (2026-04-14)

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`af77cf4`](https://github.com/camunda/orchestration-cluster-api-python/commit/af77cf43cfa6f263c6516d33ebf13379f373c282))

### Features

- Release SDK 9 for Camunda server 8.9
  ([`0e4ce04`](https://github.com/camunda/orchestration-cluster-api-python/commit/0e4ce041b20072e0f3aad72a90f7d8dc2b473087))

### Breaking Changes

- SDK major version bumped from 8 to 9 to track Camunda server 8.9


## v8.9.0-dev.37 (2026-04-14)

### Chores

- Update publishing config for release
  ([`c3392f0`](https://github.com/camunda/orchestration-cluster-api-python/commit/c3392f08da5fbe3cb5c867f511a0f3851489a41b))

- **generation**: Update generated SDK [skip ci]
  ([`d56f808`](https://github.com/camunda/orchestration-cluster-api-python/commit/d56f808b45b1b52336270e059345a254dd907e3d))

- **generation**: Update generated SDK [skip ci]
  ([`3a48faa`](https://github.com/camunda/orchestration-cluster-api-python/commit/3a48faac3e52da03444568b309bfbcdc6db172b7))

### Features

- Release SDK 9 for Camunda server 8.9BREAKING CHANGE: SDK major version bumped from 8 to 9 to track
  Camunda server 8.9
  ([`9ba3969`](https://github.com/camunda/orchestration-cluster-api-python/commit/9ba3969794af07d3e63a4caffc52c3ea6cb776fb))


## v8.9.0-dev.36 (2026-04-12)

### Bug Fixes

- Address PR #93 review comments
  ([`130703f`](https://github.com/camunda/orchestration-cluster-api-python/commit/130703fae873d97c3ecc4cc5ae810ffa9685a87f))

- Remove type: ignore suppressions by fixing root type issues
  ([`e759826`](https://github.com/camunda/orchestration-cluster-api-python/commit/e759826b09853bab086a271f478534eeb065f13c))

### Chores

- **generation**: Update generated SDK [skip ci]
  ([`5d7c8d6`](https://github.com/camunda/orchestration-cluster-api-python/commit/5d7c8d6fbe01c0303f556db1c10090be72bd1718))


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
