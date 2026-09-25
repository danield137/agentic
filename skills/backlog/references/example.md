# Backlog

Simple planning for adding reminders, offline sync, and sharing to a todo app. Start with the relevant design docs for context.

## Mandatory instructions

- Follow the Quality gate below.
- The offline sync prototype is reference material, not the implementation baseline; build sync from the main branch.
- Existing tasks must keep loading after every release; change the stored task format only together with a migration.
- Complete dependent tasks in listed order; later work waits for the evidence produced by earlier tasks.
- Record required review and integration evidence before a milestone is complete.

## Task areas

| Area | Covers |
| --- | --- |
| `TASK_LIST` | Creating, editing, completing, and ordering tasks |
| `REMINDERS` | Due dates and reminder notifications |
| `SYNC` | Offline changes and keeping tasks in sync across devices |
| `SHARING` | Sharing lists with other people and what each person can change |

## Quality gate

Use **BRCGBC** for every item: **Benchmark -> Red test -> Change/Fix -> Green test -> Benchmark -> Conformance**. Required evidence is a baseline and comparable follow-up measurement, a check that fails before and passes after the change, the change itself, and a conformance result against the stated requirements.

If a required step cannot run, keep the item open and record the blocker or approved replacement under that item. No replacement gate is currently approved; any future replacement must be named here with its required evidence and explicit benchmark and conformance substitutes.

---

* (current) [ ] **M1:** Remind people about tasks that are due
  * [ ] **REMINDERS001:** Store an optional due date and reminder time on each task
  * [ ] **REMINDERS002:** Deliver each reminder at its scheduled time
    * Note: Use the same device and conditions for both delivery-delay benchmarks.
  * [ ] **TASK_LIST004:** Sort the task list by due date
  * [ ] **REMINDERS003:** Keep reminders on time across time zone and daylight saving changes

* (next) [ ] **M2:** Keep tasks in sync across devices, including offline edits
  * [ ] **SYNC001:** Queue changes made offline and send them on reconnect
  * [ ] **SYNC002:** Resolve conflicting edits from two devices without losing either one
    * Note: Conformance evidence must cover the same task edited on two offline devices.
  * [ ] **SYNC003:** Reduce sync time for large lists on slow connections
  * [ ] **REMINDERS004:** Deliver reminders while the device is offline

* (future) [ ] **M3:** Let people share lists
  * [ ] **SHARING001:** Invite another person to a list
  * [ ] **SHARING002:** Limit what each person can change in a shared list
  * [ ] **SHARING003:** Sync shared lists between people
    * Note: Builds on the offline queue from `SYNC001`, so offline edits to a shared list aren't lost.

---

## Archive

Finished milestones whose items satisfied the Quality gate are appended here, newest last.

* (done) [x] **M0:** Ship the basic task list
  * [x] **TASK_LIST001:** Create, edit, and complete tasks
  * [x] **TASK_LIST002:** Prevent tasks with empty titles from being saved
  * [-] **TASK_LIST003:** Reorder tasks by drag and drop
    * Note: Replaced by sorting by due date in `TASK_LIST004`.
