package com.easybro92.tacodash;

// MAGA Taco Dash como app de Android (26/10/2026). El juego (la carpeta www/)
// va dentro del APK y se abre a pantalla completa en un WebView. Se sirve
// como si fuera una web (https://taco.dash/...) para que funcionen los
// modulos de JavaScript y la carga de modelos; los archivos salen del APK.

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {
  private static final String ORIGEN = "https://taco.dash/";
  private WebView web;

  @Override
  protected void onCreate(Bundle guardado) {
    super.onCreate(guardado);
    requestWindowFeature(Window.FEATURE_NO_TITLE);
    getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    web = new WebView(this);
    WebSettings s = web.getSettings();
    s.setJavaScriptEnabled(true);
    s.setDomStorageEnabled(true);
    s.setDatabaseEnabled(true);
    s.setMediaPlaybackRequiresUserGesture(false);
    s.setAllowFileAccess(false);
    web.setWebViewClient(new WebViewClient() {
      @Override
      public WebResourceResponse shouldInterceptRequest(WebView v, WebResourceRequest req) {
        String url = req.getUrl().toString();
        if (!url.startsWith(ORIGEN)) return null;      // lo de fuera (fuentes) va por internet
        String ruta = req.getUrl().getPath();
        if (ruta == null || ruta.equals("/") || ruta.isEmpty()) ruta = "/index.html";
        try {
          InputStream in = getAssets().open("www" + ruta);
          Map<String, String> cab = new HashMap<>();
          cab.put("Access-Control-Allow-Origin", "*");
          WebResourceResponse r = new WebResourceResponse(tipo(ruta), tipo(ruta).startsWith("text") || ruta.endsWith(".js") || ruta.endsWith(".json") ? "utf-8" : null, in);
          r.setResponseHeaders(cab);
          return r;
        } catch (Exception e) {
          WebResourceResponse r = new WebResourceResponse("text/plain", "utf-8", null);
          r.setStatusCodeAndReasonPhrase(404, "No existe");
          return r;
        }
      }
      @Override
      public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest req) {
        return !req.getUrl().toString().startsWith(ORIGEN);
      }
    });
    setContentView(web);
    pantallaCompleta();
    web.loadUrl(ORIGEN + "index.html");
  }

  private static String tipo(String ruta) {
    String r = ruta.toLowerCase();
    if (r.endsWith(".html")) return "text/html";
    if (r.endsWith(".js") || r.endsWith(".mjs")) return "text/javascript";
    if (r.endsWith(".css")) return "text/css";
    if (r.endsWith(".json")) return "application/json";
    if (r.endsWith(".glb")) return "model/gltf-binary";
    if (r.endsWith(".png")) return "image/png";
    if (r.endsWith(".jpg") || r.endsWith(".jpeg")) return "image/jpeg";
    if (r.endsWith(".webp")) return "image/webp";
    if (r.endsWith(".svg")) return "image/svg+xml";
    if (r.endsWith(".mp3")) return "audio/mpeg";
    if (r.endsWith(".ogg")) return "audio/ogg";
    if (r.endsWith(".wav")) return "audio/wav";
    if (r.endsWith(".wasm")) return "application/wasm";
    return "application/octet-stream";
  }

  private void pantallaCompleta() {
    web.setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
        | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
  }

  @Override
  public void onWindowFocusChanged(boolean foco) {
    super.onWindowFocusChanged(foco);
    if (foco) pantallaCompleta();
  }

  @Override
  protected void onPause() { super.onPause(); web.onPause(); }

  @Override
  protected void onResume() { super.onResume(); web.onResume(); }

  @Override
  public void onBackPressed() {
    if (web.canGoBack()) web.goBack(); else super.onBackPressed();
  }
}
