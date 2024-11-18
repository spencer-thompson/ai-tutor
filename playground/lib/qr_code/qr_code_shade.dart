import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:playground/qr_code/scanned_barcode_label.dart';
import 'package:playground/qr_code/scanner_button_widgets.dart';
import 'package:playground/qr_code/scanner_error_widget.dart';

class QrApp extends StatelessWidget {
  const QrApp({super.key});

  @override
  Widget build(BuildContext context) => const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: BarcodeScannerWithOverlay(),
      );
}

class BarcodeScannerWithOverlay extends StatefulWidget {
  const BarcodeScannerWithOverlay({super.key});

  @override
  _BarcodeScannerWithOverlayState createState() =>
      _BarcodeScannerWithOverlayState();
}

class _BarcodeScannerWithOverlayState extends State<BarcodeScannerWithOverlay> {
  final MobileScannerController controller = MobileScannerController(
    formats: const [BarcodeFormat.qrCode],
  );

  bool isCameraActive = false;

  @override
  Widget build(BuildContext context) {
    final scanWindow = Rect.fromCenter(
      center: MediaQuery.sizeOf(context).center(Offset(0, -70)),
      width: 270,
      height: 270,
    );

    return Scaffold(
      appBar: AppBar(
        title: const Center(child: Text('Scan QR Code from Extension')),
      ),
      body: Stack(
        fit: StackFit.expand,
        children: [
          Center(
            child: MobileScanner(
              //fit: BoxFit.contain,
              fit: BoxFit.cover,
              //fit: BoxFit.fitWidth,
              controller: controller,
              scanWindow: scanWindow,
              errorBuilder: (context, error, child) {
                return ScannerErrorWidget(error: error);
              },
              overlayBuilder: (context, constraints) {
                return Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Align(
                    alignment: Alignment.bottomCenter,
                    child: ScannedBarcodeLabel(barcodes: controller.barcodes),
                  ),
                );
              },
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

  @override
  Future<void> dispose() async {
    super.dispose();
    await controller.dispose();
  }
}

class ScannerOverlay extends CustomPainter {
  const ScannerOverlay({
    required this.scanWindow,
    this.borderRadius = 20.0,
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
      ..color = Colors.black.withOpacity(0.3)
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
      ..strokeWidth = 1.0;

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
