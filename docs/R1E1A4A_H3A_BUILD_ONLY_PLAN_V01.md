# H3A Build-Only Plan V0.1

Formal build target: `H3A_ORTHOGONAL_STALK_ASSEMBLY_BUILD_ONLY_V01.cst`.

This stage implements the frozen H3A architecture only. It does not optimize dimensions or RF performance.

Hard rules:
- immutable P094 parent hash lock;
- no solver;
- no RF port creation;
- no active transistor/device model;
- no dimension tuning after build output is seen;
- one formal invocation only;
- fresh-reopen CST intersection check is mandatory.

The user's currently open H2A V0.2 review window is treated as a separate interactive session and must not be closed or reused for the formal H3A build.
