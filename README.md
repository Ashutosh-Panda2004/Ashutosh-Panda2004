<div align="center">

<a href="https://www.linkedin.com/in/ashutosh2004/" target="_blank" rel="noopener noreferrer"><img src="https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/main/assets/banner.svg?v=20261007" alt="Ashutosh Panda, SDE 1 at Honeywell" width="100%" /></a>

<a href="https://shutdowncheck.vercel.app/"><img src="https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/main/assets/chip-shutdowncheck.svg" alt="ShutdownCheck live site" height="46" /></a>
<a href="https://tokenslens.vercel.app/"><img src="https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/main/assets/chip-tokenlens.svg" alt="TokenLens live site" height="46" /></a>
<a href="https://interview-coach-ai-steel.vercel.app/"><img src="https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/main/assets/chip-interviewcoach.svg" alt="InterviewCoach AI live site" height="46" /></a>

</div>

<div align="center">

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=26&duration=3000&pause=1200&color=58A6FF&center=true&vCenter=true&width=600&lines=SDE+1+at+Honeywell;Backend+systems+%C2%B7+Go+%C2%B7+TypeScript;I+build+developer+tools+in+the+open)](https://git.io/typing-svg)

[![GitHub](https://img.shields.io/badge/GitHub-171515?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ashutosh-Panda2004)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ashutosh2004/)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://ashutosh-panda-system.vercel.app/)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:ashutoshpanda.india@gmail.com)

</div>

---

## About

I'm a software development engineer at Honeywell in Bengaluru, where I'm a backend engineer on a migration platform. Before that, I was a software engineering intern at Nielsen, where I worked on a browser extension used by more than a million people.

Outside work, I build small developer tools (ShutdownCheck, TokenLens and InterviewCoach AI, below) and contribute fixes and tests to open source projects.

**Now (October 2026):** improving ShutdownCheck's release pipeline, day to day backend work at Honeywell, and open source contributions most weeks.

---

<!-- oss-highlights:start -->

## Open source highlights

65 merged pull requests · I mostly contribute to checkstyle, Apache Fineract and Eclipse SW360.

| # | Pull Request | Repo | Impact |
| --- | --- | --- | --- |
| 1 | [fix(clearingRequest): include scan-available releases in total release count](https://github.com/eclipse-sw360/sw360/pull/4672) | `eclipse-sw360/sw360` | Clearing progress no longer shows 100% while scan-available releases are still waiting; added tests for the count |
| 2 | [Fix/686 Use explicit Global allocator parameter](https://github.com/servo/rust-smallvec/pull/694) | `servo/rust-smallvec` | Made the Global allocator parameter explicit on every SmallVec use across the crate |
| 3 | [Reuse the old device ID when logging back in](https://github.com/ulyssa/iamb/pull/777) | `ulyssa/iamb` | Logout now removes the stored crypto account, so logging back in no longer fails with an account mismatch |
| 4 | [Return a copy from Engine.Get so it never writes to the cached scenario](https://github.com/sagar2395/snowopslabs/pull/86) | `sagar2395/snowopslabs` | Engine.Get returns a copy, so callers can no longer mutate the cached scenario |
| 5 | [Issue #21952: Limit exit code to 255 to avoid wrap to 0 on multiple of 256 errors](https://github.com/checkstyle/checkstyle/pull/21968) | `checkstyle/checkstyle` | The CLI exit code is now capped at 255, so a run with 256 or more errors no longer wraps to 0 and looks like a success |
| 6 | [Show finished downloads in the Downloads popover](https://github.com/beyond-all-reason/bar-lobby/pull/745) | `beyond-all-reason/bar-lobby` | Finished downloads now stay in the Downloads popover for the session instead of disappearing as soon as they complete |
| 7 | [FINERACT-2934: Merge the two force-withdrawal global configurations into a single one](https://github.com/apache/fineract/pull/6643) | `apache/fineract` | Merged the two force-withdrawal configurations into one; a database changeset copies the existing limit into the remaining configuration so existing installations keep the same behaviour |

<!-- oss-highlights:end -->

---

## Featured projects

### TokenLens

Shows what GitHub Copilot is costing you. TokenLens reads the usage data stored on your machine, breaks the spend down by project and model, forecasts the month's bill, and shows where credits are being wasted. It comes as a CLI, a local dashboard, and a VS Code extension, and nothing leaves your machine.

`TypeScript` · `Fastify` · `React` · `SQLite`

[![Live Site](https://img.shields.io/badge/Live_Site-000000?style=flat-square&logo=vercel&logoColor=white)](https://tokenslens.vercel.app/)
[![Source Code](https://img.shields.io/badge/Source_Code-171515?style=flat-square&logo=github&logoColor=white)](https://github.com/Ashutosh-Panda2004/TokensLens)

### ShutdownCheck

Checks if a service shuts down cleanly. It stops the service under real load, the way a platform like Kubernetes would, and reports which of the seven shutdown stages failed, with a named finding (SC000–SC017) and a fix for each one. Works on local processes, Docker containers, and in CI.

`Go` · `Docker` · `GitHub Actions`

[![Live Site](https://img.shields.io/badge/Live_Site-000000?style=flat-square&logo=vercel&logoColor=white)](https://shutdowncheck.vercel.app/)
[![Source Code](https://img.shields.io/badge/Source_Code-171515?style=flat-square&logo=github&logoColor=white)](https://github.com/Ashutosh-Panda2004/ShutdownCheck)

### InterviewCoach AI

Practice interviews with a voice AI. It runs live voice interviews, asks questions based on your resume, and gives feedback on your answers, including a STAR review. There is also a JavaScript practice area and a system design canvas. Your data stays in your browser.

`React 19` · `TypeScript` · `Gemini Live API` · `Express`

[![Live Site](https://img.shields.io/badge/Live_Site-000000?style=flat-square&logo=vercel&logoColor=white)](https://interview-coach-ai-steel.vercel.app/)
[![Source Code](https://img.shields.io/badge/Source_Code-171515?style=flat-square&logo=github&logoColor=white)](https://github.com/Ashutosh-Panda2004/Interviewcoach--AI)

---

## Experience

**Honeywell**, Software Development Engineer 1 · Feb 2026 – present
Backend engineer on a migration platform.

**Nielsen**, Software Engineer Intern · Jan 2025 – Feb 2026
Scaled a browser extension to 1M+ users at 99.9% uptime. Built the data checks behind it, which handled 4M+ events a day.

Six patents filed (three granted), an IEEE publication, and a Smart India Hackathon top-20 finish.

---

## Tools I work with

- **Languages:** Go, TypeScript, C#, Python, Java
- **Backend:** .NET, Node.js (Fastify, Express), Azure Service Bus
- **Frontend:** React
- **Platforms and tools:** Azure, Docker, GitHub Actions, SQLite, Git

---

## Writing

Notes on system design and engineering practice, on [Medium](https://medium.com/@ashutoshpanda.india).

---

## GitHub activity

<div align="center">

<img width="49%" src="https://github-readme-stats.vercel.app/api?username=Ashutosh-Panda2004&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=00F5FF&icon_color=00F5FF&text_color=FFFFFF&show=prs_merged" />
<img width="49%" src="https://github-readme-streak-stats.herokuapp.com/?user=Ashutosh-Panda2004&theme=tokyonight&hide_border=true&background=0D1117&ring=00F5FF&fire=00F5FF&currStreakLabel=00F5FF" />

[![Ashutosh's github activity graph](https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/output/activity-graph.svg)](https://github.com/Ashutosh-Panda2004)

![Snake animation](https://raw.githubusercontent.com/Ashutosh-Panda2004/Ashutosh-Panda2004/output/github-contribution-grid-snake-dark.svg)

</div>

---

## Contact

The quickest way to reach me is email, at [ashutoshpanda.india@gmail.com](mailto:ashutoshpanda.india@gmail.com). I'm also on [LinkedIn](https://www.linkedin.com/in/ashutosh2004/)
