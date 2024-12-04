import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:playground/header_manager.dart';
import 'package:provider/provider.dart';

class ScannedBarcodeLabel extends StatelessWidget {
  ScannedBarcodeLabel({
    super.key,
    required this.barcodes,
  });

  final Stream<BarcodeCapture> barcodes;

  @override
  Widget build(BuildContext context) {
    final headerManager = Provider.of<HeaderManager>(context);
    return StreamBuilder(
      stream: barcodes,
      builder: (context, snapshot) {
        final scannedBarcodes = snapshot.data?.barcodes ?? [];

        if (scannedBarcodes.isEmpty) {
          WidgetsBinding.instance.addPostFrameCallback(
            (_) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('No barcode scanned!'),
                  backgroundColor: Colors.redAccent,
                  duration: Duration(seconds: 2),
                ),
              );
            },
          );
          return const SizedBox.shrink();
        }

        final displayValue =
            scannedBarcodes.first.displayValue ?? 'No display value.';

        headerManager.updateHeaders(
          displayValue,
        );

        print("\n\n\n\n\n\n\n\n\n\n$displayValue\n\n\n\n\n\n\n\n\n");

        WidgetsBinding.instance.addPostFrameCallback((_) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(displayValue),
              backgroundColor: Colors.green,
              duration: const Duration(seconds: 2),
            ),
          );
        });
        return const SizedBox.shrink();
      },
    );
  }
}
