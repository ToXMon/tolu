import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";
import { createRef, ref } from "lit/directives/ref.js";

interface Terminal { write(data: string): void; }
interface PodFile {
	write(data: string | ArrayBuffer): Promise<void>;
	read(len: number): Promise<string>;
	getSize(): Promise<number>;
	close(): Promise<void>;
}
interface PodInstance {
	run(exe: string, args: string[], opts: { terminal: Terminal; env?: string[]; cwd?: string; echo?: boolean }): Promise<unknown>;
	onPortal(cb: (info: { url: string; port: number }) => void): void;
	createFile(path: string, mode: string): Promise<PodFile>;
	openFile(path: string, mode: string): Promise<PodFile>;
	createDefaultTerminal(el: HTMLElement): Promise<Terminal>;
}
interface PodSDK {
	boot(opts: { apiKey: string; storageKey?: string }): Promise<PodInstance>;
}

export type PodState = "idle" | "booting" | "running" | "error" | "disconnected";
export interface PortalInfo { url: string; port: number; }

@customElement("tolu-browser-pod")
export class ToluBrowserPod extends LitElement {
	static override styles = css`
		:host {
			display: flex; flex-direction: column;
			width: 100%; height: 100%; min-height: 200px;
			border: 1px solid var(--tc-border, #e5e7eb);
			border-radius: 8px; overflow: hidden;
			background: var(--tc-bg, #1e1e1e);
		}
		.terminal-container { flex: 1; min-height: 150px; }
		.portal-section { border-top: 1px solid var(--tc-border, #e5e7eb); background: var(--tc-surface, #252526); }
		.portal-header {
			padding: 6px 12px; font-size: 12px;
			color: var(--tc-muted, #888); display: flex; align-items: center; gap: 8px;
		}
		.portal-header a { color: var(--tc-primary, #3b82f6); text-decoration: none; word-break: break-all; }
		.portal-header a:hover { text-decoration: underline; }
		.portal-iframe { width: 100%; height: 300px; border: none; border-top: 1px solid var(--tc-border, #e5e7eb); }
		.status-bar { padding: 8px 12px; font-size: 12px; color: var(--tc-muted, #888); display: flex; align-items: center; gap: 8px; }
		.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
		.dot.booting { background: #f59e0b; } .dot.running { background: #22c55e; }
		.dot.error { background: #ef4444; } .dot.disconnected { background: #6b7280; }
		.error-msg { padding: 12px; color: #ef4444; font-family: monospace; font-size: 13px; }
	`;

	@property({ attribute: "api-key" }) apiKey?: string;
	@property({ attribute: "storage-key" }) storageKey?: string;
	@state() private _state: PodState = "idle";
	@state() private _portal: PortalInfo | null = null;
	@state() private _error: string | null = null;

	private pod: PodInstance | null = null;
	private term: Terminal | null = null;
	private termRef = createRef<HTMLDivElement>();

	get podState(): PodState { return this._state; }
	get portal(): PortalInfo | null { return this._portal; }

	override connectedCallback(): void { super.connectedCallback(); this.boot(); }
	override disconnectedCallback(): void {
		super.disconnectedCallback();
		this.pod = null; this.term = null; this._state = "disconnected";
	}

	private async boot(): Promise<void> {
		if (this.pod || this._state === "booting") return;
		const key = this.apiKey ?? import.meta.env.VITE_BROWSERPOD_API_KEY as string | undefined;
		if (!key) {
			this._state = "error";
			this._error = "API key missing. Set apiKey attr or VITE_BROWSERPOD_API_KEY.";
			return;
		}
		this._state = "booting"; this._error = null;
		try {
			const SDK: PodSDK = await import("@leaningtech/browserpod");
			const bootOpts: { apiKey: string; storageKey?: string } = { apiKey: key };
			if (this.storageKey) bootOpts.storageKey = this.storageKey;
			this.pod = await SDK.boot(bootOpts);
			this.pod.onPortal(({ url, port }: { url: string; port: number }) => {
				this._portal = { url, port };
				this.dispatchEvent(new CustomEvent("portal", { detail: { url, port } }));
			});
			this._state = "running";
			await this.updateComplete;
			const el = this.termRef.value;
			if (el && this.pod) this.term = await this.pod.createDefaultTerminal(el);
		} catch (err: unknown) {
			this._state = "error";
			this._error = err instanceof Error ? err.message : String(err);
		}
	}

	/** Run a command in the pod. */
	public async run(
		executable: string, args: string[] = [],
		opts: { cwd?: string; env?: string[]; echo?: boolean } = {},
	): Promise<unknown> {
		if (!this.pod || !this.term) throw new Error("Pod not ready. Await state 'running'.");
		return this.pod.run(executable, args, { terminal: this.term, ...opts });
	}

	/** Write a text file to the pod filesystem. */
	public async writeFile(path: string, content: string): Promise<void> {
		if (!this.pod) throw new Error("Pod not ready.");
		const f = await this.pod.createFile(path, "utf-8");
		await f.write(content); await f.close();
	}

	/** Read a text file from the pod filesystem. */
	public async readFile(path: string): Promise<string> {
		if (!this.pod) throw new Error("Pod not ready.");
		const f = await this.pod.openFile(path, "utf-8");
		const sz = await f.getSize(); const text = await f.read(sz); await f.close();
		return text;
	}

	override render() {
		if (this._state === "error") return html`<div class="error-msg">${this._error ?? "Unknown error"}</div>`;
		return html`
			${this._state === "booting" ? html`<div class="status-bar">
				<span class="dot booting"></span> Booting pod runtime…
			</div>` : ""}
			<div class="terminal-container" ${ref(this.termRef)}></div>
			${this._portal ? html`
				<div class="portal-section">
					<div class="portal-header">
						<span>Portal :${this._portal.port}</span>
						<a href=${this._portal.url} target="_blank" rel="noopener">${this._portal.url}</a>
					</div>
					<iframe class="portal-iframe" .src=${this._portal.url}
						title="Portal on port ${this._portal.port}"></iframe>
				</div>` : ""}
		`;
	}
}

declare global { interface HTMLElementTagNameMap { "tolu-browser-pod": ToluBrowserPod; } }
