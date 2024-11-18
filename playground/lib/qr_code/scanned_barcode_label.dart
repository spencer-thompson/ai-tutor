import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class ScannedBarcodeLabel extends StatelessWidget {
  const ScannedBarcodeLabel({
    super.key,
    required this.barcodes,
  });

  final Stream<BarcodeCapture> barcodes;

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: barcodes,
      builder: (context, snapshot) {
        final scannedBarcodes = snapshot.data?.barcodes ?? [];

        //if (scannedBarcodes.isEmpty) {
        //  WidgetsBinding.instance.addPostFrameCallback(
        //    (_) {
        //      ScaffoldMessenger.of(context).showSnackBar(
        //        const SnackBar(
        //          content: Text('No barcode scanned!'),
        //          backgroundColor: Colors.redAccent,
        //          duration: Duration(seconds: 2),
        //        ),
        //      );
        //    },
        //  );
        //  return const SizedBox.shrink();
        //}
        //
        //final displayValue =
        //    scannedBarcodes.first.displayValue ?? 'No display value.';
        //WidgetsBinding.instance.addPostFrameCallback((_) {
        //  ScaffoldMessenger.of(context).showSnackBar(
        //    SnackBar(
        //      content: Text(displayValue),
        //      backgroundColor: Colors.green,
        //      duration: const Duration(seconds: 200),
        //    ),
        //  );
        //});
        return const SizedBox.shrink();
      },
    );
  }
}
