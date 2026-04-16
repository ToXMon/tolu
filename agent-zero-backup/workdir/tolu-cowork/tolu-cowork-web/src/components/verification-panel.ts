import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";

export type BuildStatus = "pending" | "building" | "ready" | "failed" | "stopped";

interface TerminalLine {
	text: string;
	timestamp: number;
	stream: "stdout" | "stderr" | "system";
}

@customElement("tolu-verification-panel")
export class ToluVerificationPanel extends LitElement {
	static override styles = css`
		:host {
			display: flex; flex-direction: column;
			width: 100%; height: 100%;
			border: 1px solid var(--tc-border, #e5e7eb);
			border-radius: 8px; overflow: hidden;
			background: var(--tc-bg, #1e1e1e);
			font-family: var(--tc-font, system-ui, sans-serif);
		}
		.header {
			padding: 10px 14px; display: flex; align-items: center; gap: 10px;
			border-bottom: 1px solid var(--tc-border, #e5e7eb);
			background: var(--tc-surface, #252526);
		}
		.header .session-id {
			font-size: 12px; color: var(--tc-muted, #888);
			font-family: monospace;
		}
		.status-badge {
			font-size: 11px; padding: 2px 8px;
			border-radius: 10px; font-weight: 600;
			text-transform: uppercase; letter-spacing: 0.5px;
		}
		.status-badge.pending { background: #f59e0b22; color: #f59e0b; }
		.status-badge.building { background: #3b82f622; color: #3b82f6; }
		.status-badge.ready { background: #22c55e22; color: #22c55e; }
		.status-badge.failed { background: #ef444422; color: #ef4444; }
		.status-badge.stopped { background: #6b728022; color: #6b7280; }
		.terminal-output {
			flex: 1; overflow-y: auto; padding: 10px 14px;
			font-family: monospace; font-size: 13px;
			color: var(--tc-text, #d4d4d4); line-height: 1.6;
		}
		.terminal-output .line-stderr { color: #f87171; }
		.terminal-output .line-system { color: #93c5fd; font-style: italic; }
		.terminal-output .line-stdout { color: var(--tc-text, #d4d4d4); }
		.portal-frame {
			border-top: 1px solid var(--tc-border, #e5e7eb);
			height: 300px; width: 100%;
		}
		.portal-bar {
			padding: 6px 14px; font-size: 12px;
			color: var(--tc-muted, #888); display: flex;
			align-items: center; gap: 8px;
			border-top: 1px solid var(--tc-border, #e5e7eb);
			background: var(--tc-surface, #252526);
		}
		.portal-bar a { color: var(--tc-primary, #3b82f6); text-decoration: none; word-break: break-all; }
		.portal-bar a:hover { text-decoration: underline; }
		.empty-state {
			padding: 40px 14px; text-align: center;
			color: var(--tc-muted, #888); font-size: 14px;
		}
	`;

	@property({ attribute: "session-id" }) sessionId?: string;
	@property({ attribute: "build-status", reflect: true }) buildStatus: BuildStatus = "pending";
	@property({ attribute: "portal-url" }) portalUrl?: string;

	@state() private _lines: TerminalLine[] = [];

	/** Append a line to the terminal output. */
	public appendLine(text: string, stream: TerminalLine["stream"] = "stdout"): void {
		this._lines = [...this._lines, { text, timestamp: Date.now(), stream }];
		this.dispatchEvent(new CustomEvent("terminal-output", {
			detail: { text, stream },
		}));
	}

	/** Clear all terminal output. */
	public clearOutput(): void {
		this._lines = [];
	}

	/** Get current output as plain text. */
	public getOutput(): string {
		return this._lines.map((l) => l.text).join("\n");
	}

	private renderLines(): unknown {
		if (this._lines.length === 0) {
			return html`<div class="empty-state">Waiting for output…</div>`;
		}
		return this._lines.map(
			(line) => html`<div class="line-${line.stream}">${line.text}</div>`,
		);
	}

	override render() {
		return html`
			<div class="header">
				<span class="status-badge ${this.buildStatus}">${this.buildStatus}</span>
				${this.sessionId
					? html`<span class="session-id">${this.sessionId}</span>`
					: ""}
			</div>
			<div class="terminal-output">${this.renderLines()}</div>
			${this.portalUrl ? html`
				<div class="portal-bar">
					<span>Portal</span>
					<a href=${this.portalUrl} target="_blank" rel="noopener">${this.portalUrl}</a>
				</div>
				<iframe class="portal-frame" .src=${this.portalUrl}
					title="Verification portal preview"></iframe>
			` : ""}
		`;
	}
}

declare global { interface HTMLElementTagNameMap { "tolu-verification-panel": ToluVerificationPanel; } }
