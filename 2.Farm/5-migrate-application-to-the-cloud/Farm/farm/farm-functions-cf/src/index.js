/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

export default {
	async fetch(request) {
	  const url = new URL(request.url);
  
	  if (url.pathname === "/relay_on") {
		// xử lý bật relay
		return new Response("Relay turned ON", { status: 200 });
	  }
  
	  if (url.pathname === "/relay_off") {
		// xử lý tắt relay
		return new Response("Relay turned OFF", { status: 200 });
	  }
  
	  return new Response("Not Found", { status: 404 });
	},
  };
  
  
