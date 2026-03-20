# Lab 1 — Setup Canvas LMS 

You will **not** clone this course repository to your laptop for this lab. Instead you will **fork** it into your own GitHub space and do your work from a **small EC2 instance** in the **AWS Academy Learner Lab**.

---

## 1. Fork Canvas LMS

1. Sign in to [GitHub](https://github.com).
2. Click **Fork** (upper right) → choose your **personal** account (or an org you’re allowed to use).
3. After the fork finishes, your copy lives at `https://github.com/<your-username>/<repo-name>`.  
   **Bookmark that URL** — that is where you push branches and open pull requests if your course uses that workflow.

You do **not** need to `git clone` on your local machine for this lab; you can clone **inside** the EC2 instance in the next sections (SSH session or Remote SSH terminal).

---

## 2. AWS Academy - Learner Lab

1. Log in to [AWS Academy Login](https://awsacademy.instructure.com/) using the method provided by your school (often via Canvas or a direct Academy link).  
2. Open your **Learner Lab** for this course.
3. Click **Start Lab** (or equivalent) and wait until the lab shows **active** and exposes **AWS console** access.
4. Click **AWS** to open the **AWS Management Console** in the lab’s temporary account.  
   **Note:** Credentials and console access are **time-limited**; when the session ends, you may need to start the lab again. Save work on GitHub (push to your fork) so you don’t lose it.

---

## 3. Launch an EC2

In the AWS Console (region your instructor recommends, e.g. **us-east-1**):

1. Go to **EC2** → **Launch instance**.
2. **Name** the instance `canvas-lms`.
3. **AMI:** **Ubuntu Server** (64-bit x86), recent LTS (e.g. 22.04 or 24.04).
4. **Instance type:** a small type such as **`t3.micro`** or **`t2.micro`** (fits typical Learner Lab budgets; follow any caps your instructor gives you).
5. **Key pair:**  
   - Create **new key pair**, type **RSA** or **ED25519**, format **`.pem`**.  
   - **Download** the `.pem` file once and store it somewhere safe on the machine where you run **Cursor** or **VS Code** (your laptop). You will need it for SSH.
6. **Network settings:**  
   - Allow **SSH (port 22)** from **My IP** (recommended) or, if the lab requires it, from **0.0.0.0/0** (less secure).  
   - Follow your instructor’s security rules.
7. **Storage:** default small volume (e.g. 8–30 GB) is usually enough to start.
8. **Launch instance** and wait until its **Instance state** is **Running**.
9. Select the instance and copy its **Public IPv4 address** — you will use this as `<ip>` below.

**On the computer that has the `.pem` key** (before Remote SSH), fix permissions (macOS/Linux terminal):

```bash
chmod 400 /path/to/your-key.pem
```

On Windows, store the key in a known path; Remote SSH will reference that path in the config below.

---

## 4. Install Remote - SSH Extension 

Cursor and VS Code both support the same remote workflow.

1. Install **[Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)** from the Visual Studio Marketplace (search **Remote - SSH** in the Extensions view if needed).
2. Optional: read Microsoft’s overview: [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh).

---

## 5. SSH config for your instance

Create or edit your SSH user config file:

- **macOS / Linux:** `~/.ssh/config`
- **Windows:** `C:\Users\<YourUsername>\.ssh\config`

Add a block like this (replace placeholders with your values):

```ssh-config
Host canvas-lms
    HostName <ip>
    IdentityFile <path to pem>
    User ubuntu
```

- **`<ip>`** — the instance **Public IPv4 address** from EC2.
- **`User`** — **Ubuntu AMIs** use `ubuntu`; Amazon Linux uses `ec2-user`; other AMIs differ (check the AMI’s docs).
- **`IdentityFile`** — full path to your downloaded `.pem`**, e.g. `/Users/you/keys/my-lab.pem` or `C:\Users\you\.ssh\my-lab.pem`.
- **`Host`** — any short nickname you like; it’s the name you’ll pick in the UI.

If your key is passphrase-protected, you may use `ssh-agent` so you aren’t prompted every time; your OS or Remote SSH docs cover that.

---

## 6. Connect with Remote SSH

1. In Cursor or VS Code, open the **Command Palette** (e.g. **F1** or **Ctrl+Shift+P** / **Cmd+Shift+P**).
2. Run **Remote-SSH: Connect to Host…** and choose **`canvas-lms`** (or the **Host** name you set), or enter `ubuntu@<ip>` if you prefer.
3. When connected, use **File → Open Folder** to open a directory on the EC2 instance (e.g. your home folder or a clone of your fork).

**Clone your fork on the instance** (in the integrated terminal, after you’re connected):

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

Use a **personal access token** or **SSH keys** for GitHub if HTTPS or SSH push is required — follow GitHub’s docs and your instructor’s preference.

<% checklist
Forked course repo under your GitHub account
Learner Lab started; EC2 Ubuntu running with SSH allowed
`.pem` secured; `chmod 400` on Mac/Linux
Remote - SSH installed; `~/.ssh/config` entry works
Connected via Cursor/VS Code; can open a folder on the instance
Cloned **your fork** on EC2 (not only local)
%>

---

## Session 2 (follow-on)

For markdown systems for teams, see **[`day-2.md`](../day-2.md)**.
