package com.orbit.reportscanner

import android.annotation.SuppressLint
import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity


// Main activity for the Report Scanner app, which uses a WebView to load a web page and handle file uploads
class ReportScannerActivity: AppCompatActivity() {

    // Launcher to handle the result of file chooser activity (file picker)
    private var fileChooserResultLauncher = createFileChooserResultLauncher()

    // Callback to store the selected file URIs from the file picker
    private var fileChooserValueCallback: ValueCallback<Array<Uri>>? = null

    // This method is called when the activity is first created (initialization logic goes here)
    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_report_scanner) // Set the content view to activity_report_scanner.xml layout

        // Find the WebView by its unique ID defined in the layout file (R.id.webView)
        val webView = findViewById<WebView>(R.id.webView)

        // Load the web page URL inside the WebView (hosted via Ngrok in this case)
        webView.loadUrl("https://reliably-vocal-meerkat.ngrok-free.app/")

        // Enable JavaScript execution for the WebView (needed if the page uses JavaScript)
        webView.settings.javaScriptEnabled = true

        // Set a WebViewClient to the WebView to control what happens inside it (e.g., page navigation)
        webView.webViewClient = WebViewClient()

        // Set a custom WebChromeClient to handle advanced web interactions (like file uploads)
        webView.webChromeClient = object : WebChromeClient() {

            // This method is triggered when the web page requests to show a file chooser (e.g., <input type="file">)
            override fun onShowFileChooser(
                webView: WebView?, // The WebView initiating the file chooser
                filePathCallback: ValueCallback<Array<Uri>>?, // The callback to receive the selected file URIs
                fileChooserParams: FileChooserParams? // Parameters related to the file chooser
            ): Boolean {
                try {
                    // Save the callback so we can return the selected file URIs later
                    fileChooserValueCallback = filePathCallback

                    // Launch the file chooser activity to let the user pick a file
                    fileChooserResultLauncher.launch(fileChooserParams?.createIntent())
                } catch (e: ActivityNotFoundException) {
                    // Catch exception if no activity can handle the file chooser intent
                    e.printStackTrace() // Print the exception stack trace
                }
                return true // Return true to indicate that the file chooser was handled
            }
        }
    }

    // Function to create and register the file chooser launcher for picking files
    private fun createFileChooserResultLauncher(): ActivityResultLauncher<Intent> {
        // Register for activity result, specifying StartActivityForResult contract
        return registerForActivityResult(ActivityResultContracts.StartActivityForResult()) {
            // Check if the result of the file chooser activity is OK (file selected successfully)
            if (it.resultCode == Activity.RESULT_OK) {
                // Pass the selected file's URI back to the WebView via the callback
                fileChooserValueCallback?.onReceiveValue(arrayOf(Uri.parse(it?.data?.dataString)))
            } else {
                // If no file was selected or the result is canceled, pass null to the callback
                fileChooserValueCallback?.onReceiveValue(null)
            }
        }
    }
}
