import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:playground/basic_chat_ui.dart';
import 'package:playground/qr_code/scanned_barcode_label.dart';
import 'package:playground/qr_code/scanner_button_widgets.dart';
import 'package:playground/qr_code/scanner_error_widget.dart';

import 'package:playground/header_manager.dart';
import 'package:provider/provider.dart';

import 'package:http/http.dart' as http;

class QrApp extends StatelessWidget {
  final String? qrToken;
  final Function(String) onQrTokenUpdate;

  const QrApp({super.key, this.qrToken, required this.onQrTokenUpdate});

  @override
  Widget build(BuildContext context) {
    return BarcodeScannerWithOverlay(
      onQrCodeScanned: onQrTokenUpdate,
    );
  }
}

class BarcodeScannerWithOverlay extends StatefulWidget {
  final Function(String) onQrCodeScanned;

  const BarcodeScannerWithOverlay({super.key, required this.onQrCodeScanned});

  @override
  _BarcodeScannerWithOverlayState createState() =>
      _BarcodeScannerWithOverlayState();
}

class _BarcodeScannerWithOverlayState extends State<BarcodeScannerWithOverlay> {
  final MobileScannerController controller = MobileScannerController(
    formats: const [BarcodeFormat.qrCode],
  );

  @override
  Widget build(BuildContext context) {
    final headerManager = Provider.of<HeaderManager>(context, listen: false);
    final scanWindow = Rect.fromCenter(
      //center: MediaQuery.sizeOf(context).center(Offset.zero),
      center: MediaQuery.sizeOf(context).center(const Offset(0, -70)),
      width: 270,
      height: 270,
    );

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Scanner with Overlay Example app'),
      ),
      body: Stack(
        fit: StackFit.expand,
        children: [
          Center(
            child: MobileScanner(
              fit: BoxFit.cover,
              controller: controller,
              scanWindow: scanWindow,
              onDetect: (BarcodeCapture capture) async {
                final List<Barcode> barcodes = capture.barcodes;
                for (final barcode in barcodes) {
                  final String? code = barcode.rawValue;

                  if (code == null) {
                    continue;
                  }

                  try {
                    final isValid = await isValidQr(code);

                    if (isValid) {
                      if (mounted) {
                        await controller.stop();
                        widget.onQrCodeScanned(code);
                        headerManager.updateHeaders(code);
                        Navigator.of(context).pushReplacement(
                          MaterialPageRoute(builder: (context) => MyHomePage()),
                        );
                      }
                      break;
                    } else {
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Invalid barcode scanned!'),
                            backgroundColor: Colors.redAccent,
                            duration: Duration(seconds: 2),
                          ),
                        );
                      }
                    }
                  } catch (e) {
                    if (mounted) {
                      print(e);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Error: ${e.toString()}'),
                          backgroundColor: Colors.redAccent,
                          duration: const Duration(seconds: 2),
                        ),
                      );
                    }
                  }
                }
              },
              errorBuilder: (context, error, child) {
                return ScannerErrorWidget(error: error);
              },
              //overlayBuilder: (context, constraints) {
              //  return Padding(
              //    padding: const EdgeInsets.all(16.0),
              //    child: Align(
              //      alignment: Alignment.bottomCenter,
              //      child: ScannedBarcodeLabel(barcodes: controller.barcodes),
              //    ),
              //  );
              //},
            ),
          ),
          ValueListenableBuilder(
            valueListenable: controller,
            builder: (context, value, child) {
              if (!value.isInitialized ||
                  !value.isRunning ||
                  value.error != null) {
                return const SizedBox();
              }

              return CustomPaint(
                painter: ScannerOverlay(scanWindow: scanWindow),
              );
            },
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ToggleFlashlightButton(controller: controller),
                  SwitchCameraButton(controller: controller),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<bool> isValidQr(String? qrCode) async {
    if (qrCode == null) return false;
    final headerManager = Provider.of<HeaderManager>(context, listen: false);
    final apiKey = headerManager.apiKey ?? "";

    print('Making request with:');
    print('QR code: $qrCode');
    print('API Key: $apiKey');

    final response = await http.get(
      Uri.parse("https://api.aitutor.live/user"),
      //headers: {"Content-Type": "application/json"},
      headers: {"AITUTOR-API-KEY": apiKey, "Authorization": "Bearer ${qrCode}"},
      //body: jsonEncode({"name": "Guts"}),
    );

    print('Response status code: ${response.statusCode}');
    print('Response body: ${response.body}');

    return response.statusCode == 200;
  }

//curl https://api.aitutor.live/user -H "AITUTOR-API-KEY: <the_key>" -H "Authorization: Bearer <the_token>"

  @override
  Future<void> dispose() async {
    super.dispose();
    await controller.dispose();
  }
}

class ScannerOverlay extends CustomPainter {
  const ScannerOverlay({
    required this.scanWindow,
    this.borderRadius = 12.0,
  });

  final Rect scanWindow;
  final double borderRadius;

  @override
  void paint(Canvas canvas, Size size) {
    // we need to pass the size to the custom paint widget
    final backgroundPath = Path()
      ..addRect(Rect.fromLTWH(0, 0, size.width, size.height));

    final cutoutPath = Path()
      ..addRRect(
        RRect.fromRectAndCorners(
          scanWindow,
          topLeft: Radius.circular(borderRadius),
          topRight: Radius.circular(borderRadius),
          bottomLeft: Radius.circular(borderRadius),
          bottomRight: Radius.circular(borderRadius),
        ),
      );

    final backgroundPaint = Paint()
      ..color = Colors.black.withOpacity(0.5)
      ..style = PaintingStyle.fill
      ..blendMode = BlendMode.dstOver;

    final backgroundWithCutout = Path.combine(
      PathOperation.difference,
      backgroundPath,
      cutoutPath,
    );

    final borderPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4.0;

    final borderRect = RRect.fromRectAndCorners(
      scanWindow,
      topLeft: Radius.circular(borderRadius),
      topRight: Radius.circular(borderRadius),
      bottomLeft: Radius.circular(borderRadius),
      bottomRight: Radius.circular(borderRadius),
    );

    const topGradient = LinearGradient(
        colors: [Colors.transparent, Colors.black],
        begin: Alignment.bottomCenter,
        end: Alignment.topCenter);

    const bottomGradient = LinearGradient(
        colors: [Colors.black, Colors.transparent],
        begin: Alignment.bottomCenter,
        end: Alignment.topCenter);

    const double gradientHeight = 200.0;
    final double gradientWidth = size.width;

    final gradientBorderPaintTop = Paint()
      ..shader = topGradient
          .createShader(Rect.fromLTWH(0, 0, gradientWidth, gradientHeight));

    final gradientBorderPaintBottom = Paint()
      ..shader = bottomGradient.createShader(Rect.fromLTWH(
          0, size.height - 400, size.width, gradientHeight + 100));

    final topBorderRect = RRect.fromRectAndCorners(
      Rect.fromLTRB(0, 0, gradientWidth, gradientHeight),
    );

    final bottomBorderRect = RRect.fromRectAndCorners(
      Rect.fromLTRB(0, size.height, gradientWidth, -gradientHeight - 300),
    );

    final rect = RRect.fromRectAndCorners(Rect.fromLTRB(
        0, size.height, gradientWidth, size.height - gradientHeight));

    final painting = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill
      ..strokeWidth = 1.0;

    // First, draw the background,
    // with a cutout area that is a bit larger than the scan window.
    // Finally, draw the scan window itself.
    canvas.drawPath(backgroundWithCutout, backgroundPaint);
    canvas.drawRRect(borderRect, borderPaint);
    canvas.drawRRect(topBorderRect, gradientBorderPaintTop);
    canvas.drawRRect(bottomBorderRect, gradientBorderPaintBottom);
    //canvas.drawRRect(rect, painting);
  }

  @override
  bool shouldRepaint(ScannerOverlay oldDelegate) {
    return scanWindow != oldDelegate.scanWindow ||
        borderRadius != oldDelegate.borderRadius;
  }
}
