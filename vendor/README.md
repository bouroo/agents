# vendor/

Third-party skill sources are mounted as git submodules and surfaced into `skills/` by an untracked relative symlink. The repository stores only a pointer — the gitlink, the upstream URL, and this file — never third-party content. `scripts/check.py` skips symlinked skill directories, so vendored content stays outside every gate.

## ai-skill — drawio-hla-architect

- Upstream: https://github.com/Jdemon/ai-skill (`main`)
- Submodule URL: https://github.com/bouroo/ai-skill (fork; it serves the pinned local branch)
- Pin: gitlink `vendor/ai-skill`, branch `improve/layout-quality`
- Surface, create locally once: `ln -s ../vendor/ai-skill/drawio-hla-architect skills/drawio-hla-architect`
- The symlink is deliberately untracked: a tracked symlink would ship third-party content under this repository's name, and a gitlink under `skills/` has no `SKILL.md` on a clean clone. The `thirdparty` gate checks that the pointer is untracked, resolvable, and documented here with a URL.
- Local improvements live on `improve/layout-quality` inside the submodule. The branch carries spec conformance on top of upstream `main`: a flat, identity-free `description`, and detail split into `references/` with stated load conditions.
- Sync upstream: `git -C vendor/ai-skill remote add upstream https://github.com/Jdemon/ai-skill.git`, then `git -C vendor/ai-skill fetch upstream && git -C vendor/ai-skill merge upstream/main`. Re-run `python3 vendor/ai-skill/drawio-hla-architect/scripts/qa_verify_hla.py <sample>.drawio --strict`, push the branch to the fork, then commit the new pin here.
- Do not run `git submodule update --remote`: it checks out the fetched default branch and drops the local branch.
- Branch-local by design (AGENTS.md §10): upstream content may carry real-work identity, so it lives in the submodule and is documented here rather than copied. Never copy upstream files into tracked, non-submodule paths.
- CI checks out without `submodules`, so vendored content never enters a gate run. That is the intended boundary, not a coverage gap.
