<div align="center">

<img src="./header.svg?v=11" width="860" alt="Ashutosh Panda, backend engineer from Bengaluru" />

<br><br>

<table>
  <tr>
    <td valign="top"><img src="./ascii-portrait.svg?v=10" width="370" alt="ASCII portrait of Ashutosh Panda" /></td>
    <td valign="top"><img src="./info-card.svg?v=10" width="490" alt="neofetch style card: role, stack and live GitHub stats" /></td>
  </tr>
</table>

<br>

<table>
  <tr>
    <td valign="top"><img src="./globe.svg?v=10" width="430" alt="Rotating 3D globe with arcs from Bengaluru to the open source projects I contribute to" /></td>
    <td valign="top"><img src="./tech-sphere.svg?v=10" width="430" alt="Tech stack on a rotating 3D sphere" /></td>
  </tr>
</table>

<br>

<img src="./github-activity.svg?v=10" width="860" alt="GitHub activity: contributions by type, 130 merged pull requests, streaks and weekly activity" />

</div>

<div align="center">

<br>

<img src="./contrib-skyline.svg?v=10" width="860" alt="Isometric 3D skyline of the last year of contributions" />

<br><br>

<img src="./contrib-heatmap.svg?v=10" width="860" alt="Contribution heatmap for the last year" />

<br><br>

</div>

<!-- oss-highlights:start -->

## Open source highlights

130 merged pull requests · I mostly contribute to checkstyle, Apache Fineract and rust-smallvec.

| # | Pull Request | Repo | Impact |
| --- | --- | --- | --- |
| 1 | [Issue #22166: Fix OneStatementPerLineCheck not clearing state on beginTree](https://github.com/checkstyle/checkstyle/pull/22380) | `checkstyle/checkstyle` | OneStatementPerLineCheck now clears its state at the start of each file, so violations no longer carry over into the next file. |
| 2 | [Issue #21952: Limit exit code to 255 to avoid wrap to 0 on multiple of 256 errors](https://github.com/checkstyle/checkstyle/pull/21968) | `checkstyle/checkstyle` | The CLI exit code is now capped at 255, so a run with a multiple of 256 errors no longer exits as success. |
| 3 | [Issue #22173: MethodCountCheck does not clear counters on beginTree](https://github.com/checkstyle/checkstyle/pull/22178) | `checkstyle/checkstyle` | MethodCountCheck now resets its counters at the start of each file instead of counting across files. |
| 4 | [TRUNK-6848: Reject invalid dates and times in Obs.setValueAsString for DT and TM datatypes](https://github.com/openmrs/openmrs-core/pull/6732) | `openmrs/openmrs-core` | Invalid date and time strings are now rejected when setting observation values, instead of being stored. |
| 5 | [FINERACT-2934: Merge the two force-withdrawal global configurations into a single one](https://github.com/apache/fineract/pull/6643) | `apache/fineract` | Two separate force-withdrawal global configurations were merged into a single one. |
| 6 | [fix(clearingRequest): include scan-available releases in total release count](https://github.com/eclipse-sw360/sw360/pull/4672) | `eclipse-sw360/sw360` | The total release count for a clearing request now includes releases that are available from a scan. |
| 7 | [FINERACT-2908: Withhold tax when the Post Interest For Savings job posts interest](https://github.com/apache/fineract/pull/6614) | `apache/fineract` | The Post Interest For Savings job now withholds tax when posting interest, with the matching journal entries, instead of skipping it. |

<!-- oss-highlights:end -->
